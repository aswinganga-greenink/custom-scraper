from __future__ import annotations
from typing import Generator

from .element import HTMLElement


# ── Private helper ────────────────────────────────────────────────────────────

def _extract_html(token_id: int, node_list: list, nodes: dict, body: str) -> str:
    """
    Slice the raw HTML string for a given open_tag token using the character
    offsets that the lexer stored in every token.

    Cases:
      - Normal element  →  body[open.start : close_tag.end]
      - Self-closing    →  closing_at == token_id  →  body[open.start : open.end]
      - Unclosed tag    →  closing_at == 0         →  body[open.start : open.end]
    """
    open_token = node_list[token_id]
    closing_at = nodes[token_id]["closing_at"]

    if closing_at == token_id or closing_at == 0:
        end_offset = open_token["end"]
    else:
        end_offset = node_list[closing_at]["end"]

    return body[open_token["start"]:end_offset]


# ── HTMLDocument ──────────────────────────────────────────────────────────────

class HTMLDocument:
    """
    Represents the fully parsed HTML document.

    Accepts the raw output of the existing lexer / html_parser pipeline and
    builds a proper tree of HTMLElement objects.  Exposes the same
    get_by_tag / get_by_class / get_by_id API as HTMLElement, but searches
    the entire document.

    Usage
    -----
        node_list = attr_tokenizer(lexer(body))
        nodes     = html_parser(node_list)
        doc       = HTMLDocument(node_list, nodes, body)

        links     = doc.get_by_tag("a")
        sidebar   = doc.get_by_id("sidebar")
        nav_links = sidebar.get_by_tag("a")   # scoped to sidebar only
    """

    def __init__(self, node_list: list, nodes: dict, body: str):
        self._body:     str                      = body
        self._roots:    list[HTMLElement]        = []
        self._elements: dict[int, HTMLElement]   = {}
        self._build_tree(node_list, nodes, body)

    # ── Tree construction ─────────────────────────────────────────────────────

    def _build_tree(self, node_list: list, nodes: dict, body: str) -> None:
        """
        Two-pass build:
          Pass 1 — create an HTMLElement for every open_tag in the node list.
          Pass 2 — wire up parent ↔ child references using the nodes dict.
        """
        # Pass 1: instantiate elements
        for token in node_list:
            if token["type"] != "open_tag":
                continue

            token_id = token["id"]
            if token_id not in nodes:
                continue

            attrs = token.get("attribute", {})
            if not isinstance(attrs, dict):
                attrs = {}

            html = _extract_html(token_id, node_list, nodes, body)

            el = HTMLElement(
                tag=token["value"],
                attributes=attrs,
                html=html,
                token_id=token_id,
            )
            self._elements[token_id] = el

        # Pass 2: wire parent ↔ child
        for token_id, el in self._elements.items():
            parent_id = nodes[token_id]["parent"]

            if parent_id == 0 or parent_id not in self._elements:
                # top-level node (html, head, body, or orphaned element)
                self._roots.append(el)
            else:
                self._elements[parent_id]._add_child(el)

    # ── Internal traversal ────────────────────────────────────────────────────

    def _walk(self) -> Generator[HTMLElement, None, None]:
        """Yield every element in the document (depth-first)."""
        for root in self._roots:
            yield root
            yield from root._walk()

    # ── Public query API ──────────────────────────────────────────────────────

    def get_by_tag(self, tag_name: str) -> list[HTMLElement]:
        """Return all elements in the document matching tag_name (case-insensitive)."""
        target = tag_name.lower().strip()
        return [el for el in self._walk() if el.tag.lower() == target]

    def get_by_class(self, class_name: str) -> list[HTMLElement]:
        """
        Return all elements whose class attribute contains class_name.
        Handles multi-class strings like class="btn active primary".
        """
        results = []
        for el in self._walk():
            if class_name in el.attributes.get("class", "").split():
                results.append(el)
        return results

    def get_by_id(self, id_value: str) -> HTMLElement | None:
        """
        Return the first element whose id attribute matches id_value exactly.
        Returns None if not found.
        """
        for el in self._walk():
            if el.attributes.get("id", "") == id_value:
                return el
        return None

    # ── Public properties ─────────────────────────────────────────────────────

    @property
    def body(self) -> str:
        """The raw HTML body string this document was built from."""
        return self._body

    @property
    def roots(self) -> list[HTMLElement]:
        """Top-level elements (those with no parent in the parse tree)."""
        return list(self._roots)

    # ── Dunder ────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"<HTMLDocument"
            f" roots={len(self._roots)}"
            f" total_elements={len(self._elements)}>"
        )
