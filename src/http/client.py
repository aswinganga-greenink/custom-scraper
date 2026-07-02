from __future__ import annotations
import socket as s
from src.resolveDNS import resolve_dns
from src.htmlParser import make_dict, length_parser, chunk_parser


class HTTPResponse:
    """
    Thin wrapper around the raw HTTP response.

    Attributes
    ----------
    status_code : int
    status_text : str
    headers     : dict
    body        : str
    """

    def __init__(self, data: dict):
        self._data = data

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

    def __repr__(self) -> str:
        return f"<HTTPResponse {self.status_code} {self.status_text}>"


class HTTPClient:
    """
    Minimal HTTP/1.1 GET client over raw TCP sockets. No dependencies.

    Usage
    -----
        client   = HTTPClient(timeout=10)
        response = client.get("example.com")
        print(response.status_code)   # 200
        print(response.body[:200])    # raw HTML
    """

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def get(self, domain: str, path: str = "/", port: int = 80) -> HTTPResponse:
        """
        Perform an HTTP GET request.

        Parameters
        ----------
        domain  : str   e.g. "neverssl.com"
        path    : str   URL path, default "/"
        port    : int   TCP port, default 80

        Returns
        -------
        HTTPResponse
        """
        ips = resolve_dns(domain)

        fd = s.socket(s.AF_INET, s.SOCK_STREAM)
        fd.settimeout(self.timeout)
        fd.connect((ips[0], port))

        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {domain}\r\n"
            f"User-Agent: greenink-scraper/0.3\r\n"
            f"Connection: close\r\n\r\n"
        )
        fd.send(request.encode())

        # Read the initial chunk (headers + start of body)
        raw = fd.recv(4096)
        str_response = raw.decode("utf8", errors="ignore")
        data = str_response.split("\r\n\r\n", 1)

        header, http_meta = make_dict(data[0])
        body = data[1] if len(data) == 2 else ""

        header_keys = header.keys()

        if "Content-Length" in header_keys and "Transfer-Encoding" not in header_keys:
            remaining = int(header["Content-Length"]) - len(body)
            if remaining > 0:
                body += length_parser(fd, remaining)

        elif "Transfer-Encoding" in header_keys:
            if header["Transfer-Encoding"] == "chunked" and "\r\n\r\n" not in body:
                body += chunk_parser(fd)

        else:
            try:
                body_len = int(header.get("Content-Length", 0))
                if body_len > 0:
                    body = length_parser(fd, body_len)
            except (ValueError, TypeError):
                pass

        fd.close()

        http_meta["header"] = header
        http_meta["body"] = body

        return HTTPResponse(http_meta)
