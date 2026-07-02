def _extract_html(token_id: int, node_list: list, nodes: dict, body: str) -> str:
    """
    Extract the raw HTML string for a given open_tag token id.
    Uses character offsets stored in the lexer tokens.
    """
    open_token = node_list[token_id]
    closing_at = nodes[token_id]["closing_at"]

    # Self-closing / void tag  →  closing_at == token_id
    # Unclosed tag             →  closing_at == 0
    # Both cases: slice up to the end of the open tag itself
    if closing_at == token_id or closing_at == 0:
        end_offset = open_token["end"]
    else:
        end_offset = node_list[closing_at]["end"]

    return body[open_token["start"]:end_offset]


def _build_result(token: dict, node: dict, html: str) -> dict:
    """Build a uniform result dict for every query function."""
    return {
        "tag":        token["value"],
        "id":         token["id"],
        "attributes": token.get("attribute", {}),
        "parent_id":  node.get("parent", 0),
        "children":   node.get("child", []),
        "html":       html,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_by_class(class_name: str, node_list: list, nodes: dict, body: str) -> list[dict]:
    """
    Return all elements whose 'class' attribute contains *class_name*.
    Handles multi-class values like class="btn active primary".
    """
    results = []

    for token in node_list:
        if token["type"] != "open_tag":
            continue

        attrs = token.get("attribute", {})
        if not isinstance(attrs, dict):
            continue

        raw_class = attrs.get("class", "")
        classes = raw_class.split()          # split on any whitespace

        if class_name in classes:
            token_id = token["id"]
            html = _extract_html(token_id, node_list, nodes, body)
            results.append(_build_result(token, nodes[token_id], html))

    return results


def get_by_id(id_value: str, node_list: list, nodes: dict, body: str) -> dict | None:
    """
    Return the first element whose 'id' attribute matches *id_value* exactly.
    Returns None if not found (ids are supposed to be unique in valid HTML).
    """
    for token in node_list:
        if token["type"] != "open_tag":
            continue

        attrs = token.get("attribute", {})
        if not isinstance(attrs, dict):
            continue

        if attrs.get("id", "") == id_value:
            token_id = token["id"]
            html = _extract_html(token_id, node_list, nodes, body)
            return _build_result(token, nodes[token_id], html)

    return None


def get_by_tag(tag_name: str, node_list: list, nodes: dict, body: str) -> list[dict]:
    """
    Return all elements whose tag matches *tag_name* (case-insensitive).
    e.g. get_by_tag("a", ...) returns every <a> anchor element.
    """
    tag_lower = tag_name.lower().strip()
    results = []

    for token in node_list:
        if token["type"] != "open_tag":
            continue

        if token["value"].lower() == tag_lower:
            token_id = token["id"]
            html = _extract_html(token_id, node_list, nodes, body)
            results.append(_build_result(token, nodes[token_id], html))

    return results
