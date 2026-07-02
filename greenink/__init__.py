"""
greenink-scraper
~~~~~~~~~~~~~~~~
A from-scratch web crawler with an HTML lexer, parse-tree builder,
and OOP DOM query API.  No third-party dependencies.

Quickstart::

    from greenink import HTTPClient, HTMLParser

    client   = HTTPClient()
    response = client.get("example.com")
    doc      = HTMLParser.parse(response.body)

    for link in doc.get_by_tag("a"):
        print(link.text, "→", link.attributes.get("href"))
"""

from greenink.http.client import HTTPClient, HTTPResponse
from greenink.parser import HTMLParser
from greenink.dom import HTMLDocument, HTMLElement

__version__ = "0.3.0"
__all__ = [
    "HTTPClient",
    "HTTPResponse",
    "HTMLParser",
    "HTMLDocument",
    "HTMLElement",
]
