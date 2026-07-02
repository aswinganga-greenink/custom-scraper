from greenink.lexer import lexer, attr_tokenizer
from greenink.htmlParser import html_parser
from greenink.dom import HTMLDocument


class HTMLParser:
    """
    Facade that wraps the full lexer → parser → DOM pipeline into one call.

    Usage
    -----
        doc = HTMLParser.parse(html_string)
        links = doc.get_by_tag("a")
    """

    @staticmethod
    def parse(html: str) -> HTMLDocument:
        """
        Parse a raw HTML string and return a queryable HTMLDocument.

        Parameters
        ----------
        html : str
            Raw HTML body text.

        Returns
        -------
        HTMLDocument
        """
        node_list = lexer(html)
        node_list = attr_tokenizer(node_list)
        nodes = html_parser(node_list)
        return HTMLDocument(node_list, nodes, html)
