"""
faircrawler.http.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Custom exception hierarchy for Fair Crawler's HTTP layer.
All exceptions inherit from FairCrawlerError for easy broad catching.
"""


class FairCrawlerError(Exception):
    """Base exception for all Fair Crawler errors."""


class ConnectionError(FairCrawlerError):
    """Raised when the TCP connection to the server fails."""


class TooManyRedirectsError(FairCrawlerError):
    """Raised when the redirect chain exceeds max_redirects."""

    def __init__(self, url: str, limit: int):
        super().__init__(f"Exceeded {limit} redirects while fetching: {url}")
        self.url   = url
        self.limit = limit


class SSLVerificationError(FairCrawlerError):
    """Raised when SSL certificate verification fails."""

    def __init__(self, host: str, reason: str = ""):
        msg = f"SSL verification failed for '{host}'"
        if reason:
            msg += f": {reason}"
        super().__init__(msg)
        self.host = host
