"""
faircrawler.http.url
~~~~~~~~~~~~~~~~~~~~
URL parsing for Fair Crawler.

Uses Python's stdlib urllib.parse under the hood — no extra dependencies.
Handles all common forms:

    URL("https://example.com/path?q=1")
    URL("http://example.com")
    URL("example.com")          ← assumes http://
"""

from __future__ import annotations
from urllib.parse import urlparse, urlencode, urlunparse


class URL:
    """
    Represents a parsed HTTP/HTTPS URL.

    Attributes
    ----------
    scheme   : "http" or "https"
    host     : hostname without port  e.g. "example.com"
    port     : int  (80 for http, 443 for https, or explicit)
    path     : str  including query string  e.g. "/search?q=foo"
    is_secure: bool  True for https
    raw      : the original string passed in

    Examples
    --------
        u = URL("https://example.com/about")
        u.scheme    # "https"
        u.host      # "example.com"
        u.port      # 443
        u.path      # "/about"
        u.is_secure # True
    """

    _DEFAULT_PORTS = {"http": 80, "https": 443}

    def __init__(self, raw: str):
        self.raw = raw

        # Normalise — add scheme if missing so urlparse works correctly
        normalized = raw
        if "://" not in normalized:
            normalized = "http://" + normalized

        parsed = urlparse(normalized)

        self.scheme: str = parsed.scheme.lower() or "http"
        self.host:   str = parsed.hostname or ""
        self.port:   int = parsed.port or self._DEFAULT_PORTS.get(self.scheme, 80)

        # Reconstruct path + query string
        self.path: str = parsed.path or "/"
        if parsed.query:
            self.path += "?" + parsed.query
        if parsed.fragment:          # fragments are not sent to the server
            pass

    # ── Derived ──────────────────────────────────────────────────────────────

    @property
    def is_secure(self) -> bool:
        """True if the scheme is https."""
        return self.scheme == "https"

    @property
    def origin(self) -> str:
        """scheme + host + port  e.g. 'https://example.com:8443'"""
        default = self._DEFAULT_PORTS.get(self.scheme)
        port_str = f":{self.port}" if self.port != default else ""
        return f"{self.scheme}://{self.host}{port_str}"

    # ── Relative URL resolution ───────────────────────────────────────────────

    def resolve(self, location: str) -> URL:
        """
        Resolve a redirect Location header relative to this URL.

        Handles:
          - Absolute URLs   "https://other.com/page"
          - Root-relative   "/new/path"
          - Relative        "subpage"
        """
        if "://" in location:
            # Fully absolute — use as-is
            return URL(location)

        if location.startswith("/"):
            # Root-relative — same origin, new path
            return URL(f"{self.origin}{location}")

        # Relative — resolve against current directory
        base_path = self.path.rsplit("/", 1)[0] + "/"
        return URL(f"{self.origin}{base_path}{location}")

    # ── Dunder ───────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"<URL {self.scheme}://{self.host}:{self.port}{self.path}>"

    def __str__(self) -> str:
        return f"{self.origin}{self.path}"
