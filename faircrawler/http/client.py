"""
faircrawler.http.client
~~~~~~~~~~~~~~~~~~~~~~~
HTTP/HTTPS client over raw TCP sockets.
Supports TLS (via stdlib ssl), automatic redirect following,
and configurable SSL verification.
"""

from __future__ import annotations
import socket as s
import ssl

from faircrawler.resolveDNS import resolve_dns
from faircrawler.htmlParser import make_dict, length_parser, chunk_parser
from faircrawler.http.url import URL
from faircrawler.http.exceptions import (
    TooManyRedirectsError,
    SSLVerificationError,
    ConnectionError,
)

# HTTP status codes that trigger a redirect
_REDIRECT_CODES = {301, 302, 303, 307, 308}


class HTTPResponse:
    """
    Typed wrapper around a raw HTTP response.

    Attributes
    ----------
    status_code : int
    status_text : str
    headers     : dict[str, str]
    body        : str
    url         : URL   — the final URL after any redirects
    """

    def __init__(self, data: dict, url: URL):
        self._data = data
        self.url   = url

    @property
    def status_code(self) -> int:
        return int(self._data.get("status_code", 0))

    @property
    def status_text(self) -> str:
        return self._data.get("status_text", "")

    @property
    def headers(self) -> dict:
        return self._data.get("header", {})

    @property
    def body(self) -> str:
        return self._data.get("body", "")

    @property
    def ok(self) -> bool:
        """True if status_code is 2xx."""
        return 200 <= self.status_code < 300

    def __repr__(self) -> str:
        return f"<HTTPResponse {self.status_code} {self.status_text} url={self.url}>"


class HTTPClient:
    """
    Minimal HTTP/1.1 + HTTPS client. No third-party dependencies.

    Parameters
    ----------
    timeout      : socket timeout in seconds (default 10)
    max_redirects: how many 3xx redirects to follow before raising (default 5)
    verify_ssl   : validate server certificate (default True)

    Usage
    -----
        client = HTTPClient()

        # HTTP
        r = client.get("http://example.com")

        # HTTPS
        r = client.get("https://example.com")

        # Bare domain — assumes http://
        r = client.get("example.com")

        print(r.status_code, r.ok)
        print(r.body[:200])
    """

    def __init__(
        self,
        timeout: int = 10,
        max_redirects: int = 5,
        verify_ssl: bool = True,
    ):
        self.timeout       = timeout
        self.max_redirects = max_redirects
        self.verify_ssl    = verify_ssl

    # ── Public API ────────────────────────────────────────────────────────────

    def get(self, url: str, path: str = "/") -> HTTPResponse:
        """
        Perform an HTTP GET request.

        Parameters
        ----------
        url  : Full URL ("https://example.com/path") or bare domain ("example.com")
        path : Used only when url is a bare domain with no path info

        Returns
        -------
        HTTPResponse
        """
        # Build the URL object — attach path if only a domain was given
        if "://" not in url and "/" not in url.split(".")[-1]:
            parsed = URL(url + path)
        else:
            parsed = URL(url)

        return self._fetch(parsed, redirects_remaining=self.max_redirects)

    # ── Internal ──────────────────────────────────────────────────────────────

    def _make_ssl_context(self) -> ssl.SSLContext:
        if self.verify_ssl:
            ctx = ssl.create_default_context()
        else:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.check_hostname = False
            ctx.verify_mode    = ssl.CERT_NONE
        return ctx

    def _open_socket(self, url: URL) -> s.socket | ssl.SSLSocket:
        """Resolve DNS, connect, optionally wrap with TLS."""
        try:
            ips = resolve_dns(url.host)
            sock = s.socket(s.AF_INET, s.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((ips[0], url.port))
        except (s.error, OSError) as e:
            raise ConnectionError(f"Cannot connect to {url.host}:{url.port} — {e}") from e

        if url.is_secure:
            try:
                ctx  = self._make_ssl_context()
                sock = ctx.wrap_socket(sock, server_hostname=url.host)
            except ssl.SSLCertVerificationError as e:
                sock.close()
                raise SSLVerificationError(url.host, str(e)) from e
            except ssl.SSLError as e:
                sock.close()
                raise SSLVerificationError(url.host, str(e)) from e

        return sock

    def _send_request(self, sock: s.socket, url: URL) -> str:
        """Send GET request and return the full raw response string."""
        request = (
            f"GET {url.path} HTTP/1.1\r\n"
            f"Host: {url.host}\r\n"
            f"User-Agent: fair-crawler/0.4\r\n"
            f"Accept: text/html,application/xhtml+xml,*/*\r\n"
            f"Connection: close\r\n\r\n"
        )
        sock.send(request.encode())

        raw = sock.recv(4096)
        return raw.decode("utf8", errors="ignore")

    def _read_body(self, sock: s.socket, header: dict, partial_body: str) -> str:
        """Read remaining body bytes based on Content-Length or chunked encoding."""
        header_keys = header.keys()

        if "Content-Length" in header_keys and "Transfer-Encoding" not in header_keys:
            remaining = int(header["Content-Length"]) - len(partial_body)
            if remaining > 0:
                partial_body += length_parser(sock, remaining)

        elif "Transfer-Encoding" in header_keys:
            te = header["Transfer-Encoding"].lower()
            if te == "chunked" and "\r\n\r\n" not in partial_body:
                partial_body += chunk_parser(sock)

        else:
            try:
                body_len = int(header.get("Content-Length", 0))
                if body_len > 0:
                    partial_body = length_parser(sock, body_len)
            except (ValueError, TypeError):
                pass

        return partial_body

    def _fetch(self, url: URL, redirects_remaining: int) -> HTTPResponse:
        """Core fetch — opens socket, sends request, handles redirects."""
        sock = self._open_socket(url)

        try:
            str_response = self._send_request(sock, url)
            data = str_response.split("\r\n\r\n", 1)

            header, http_meta = make_dict(data[0])
            partial_body      = data[1] if len(data) == 2 else ""
            body              = self._read_body(sock, header, partial_body)
        finally:
            sock.close()

        http_meta["header"] = header
        http_meta["body"]   = body

        response = HTTPResponse(http_meta, url=url)

        # ── Redirect handling ─────────────────────────────────────────────────
        if response.status_code in _REDIRECT_CODES:
            location = header.get("Location", "").strip()

            if not location:
                return response     # no Location header — return as-is

            if redirects_remaining <= 0:
                raise TooManyRedirectsError(str(url), self.max_redirects)

            next_url = url.resolve(location)
            return self._fetch(next_url, redirects_remaining - 1)

        return response
