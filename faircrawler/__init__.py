"""
fair-crawler
~~~~~~~~~~~~~~~~
A from-scratch web crawler with an HTML lexer, parse-tree builder,
and OOP DOM query API.  No third-party dependencies.

Quickstart::

    from faircrawler import HTTPClient, HTMLParser

    client   = HTTPClient()
    response = client.get("example.com")
    doc      = HTMLParser.parse(response.body)

    for link in doc.get_by_tag("a"):
        print(link.text, "→", link.attributes.get("href"))
"""

from faircrawler.http.client import HTTPClient, HTTPResponse
from faircrawler.http.url import URL
from faircrawler.http.exceptions import (
    FairCrawlerError,
    TooManyRedirectsError,
    SSLVerificationError,
)
from faircrawler.parser import HTMLParser
from faircrawler.dom import HTMLDocument, HTMLElement

__version__ = "0.4.0"
__all__ = [
    "HTTPClient",
    "HTTPResponse",
    "URL",
    "HTMLParser",
    "HTMLDocument",
    "HTMLElement",
    "FairCrawlerError",
    "TooManyRedirectsError",
    "SSLVerificationError",
]
