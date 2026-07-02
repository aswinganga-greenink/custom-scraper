from __future__ import annotations
from typing import Generator


class HTMLElement:
    """
    Represents a single HTML element node in the parse tree.

    After an HTMLDocument is built, every open_tag becomes one of these.
    Elements hold a reference to their parent and a list of their direct
    children, enabling scoped, chainable queries:

        table = doc.get_by_id("results-table")
        rows  = table.get_by_tag("tr")   # only searches inside the table
    """

    def __init__(self, tag: str, attributes: dict, html: str, token_id: int):
        self.tag        = tag           # e.g. "a", "div", "h1"
        self.attributes = attributes    # parsed attr dict from lexer
        self.html       = html          # raw HTML slice from the original body
        self.token_id   = token_id      # original lexer id (useful for debugging)

        self._children: list[HTMLElement] = []
        self._parent:   HTMLElement | None = None

    # ── Tree linkage (called by HTMLDocument._build_tree) ────────────────────

    def _add_child(self, child: HTMLElement) -> None:
        child._parent = self
        self._children.append(child)

    # ── Public properties ────────────────────────────────────────────────────

    @property
    def parent(self) -> HTMLElement | None:
        """Direct parent element, or None if this is a root node."""
        return self._parent

    @property
    def children(self) -> list[HTMLElement]:
        """Shallow copy of direct child elements."""
        return list(self._children)

    @property
    def text(self) -> str:
        """
        Concatenated visible text content of this element (all tags stripped).
        Useful for quickly reading anchor text, headings, etc.
        """
        import re
        return re.sub(r"<[^>]+>", "", self.html).strip()

    # ── Internal depth-first traversal ───────────────────────────────────────

    def _walk(self) -> Generator[HTMLElement, None, None]:
        """Yield every descendant in depth-first order (self NOT included)."""
        for child in self._children:
            yield child
            yield from child._walk()

    # ── Scoped query API ─────────────────────────────────────────────────────

    def get_by_tag(self, tag_name: str) -> list[HTMLElement]:
        """
        Return all *descendant* elements matching tag_name (case-insensitive).
        Only searches within this element's subtree.
        """
        target = tag_name.lower().strip()
        return [el for el in self._walk() if el.tag.lower() == target]

    def get_by_class(self, class_name: str) -> list[HTMLElement]:
        """
        Return all *descendant* elements whose class attribute contains
        class_name.  Handles multi-class values like "btn active primary".
        """
        results = []
        for el in self._walk():
            if class_name in el.attributes.get("class", "").split():
                results.append(el)
        return results

    def get_by_id(self, id_value: str) -> HTMLElement | None:
        """
        Return the first *descendant* element whose id attribute matches
        id_value exactly.  Returns None if not found.
        """
        for el in self._walk():
            if el.attributes.get("id", "") == id_value:
                return el
        return None

    # ── Dunder ───────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        attrs_str = ""
        if isinstance(self.attributes, dict):
            parts = [f'{k}="{v}"' for k, v in list(self.attributes.items())[:3]]
            attrs_str = (" " + " ".join(parts)) if parts else ""
        return (
            f"<HTMLElement <{self.tag}{attrs_str}>"
            f" children={len(self._children)}>"
        )
