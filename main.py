from src.tcpConn import create_connection, get_http_response
from src.lexer import lexer, attr_tokenizer
from src.htmlParser import make_dict, html_parser
from src.query import get_by_class, get_by_id, get_by_tag

domain = "neverssl.com"

# ── Fetch & parse ────────────────────────────────────────────────────────────
fd       = create_connection(domain)
response = get_http_response(fd, domain)
body     = response["body"]

node_list = lexer(body)
node_list = attr_tokenizer(node_list)
nodes     = html_parser(node_list)

# ── Query by TAG ─────────────────────────────────────────────────────────────
print("=" * 60)
print("get_by_tag('a')")
print("=" * 60)
anchors = get_by_tag("a", node_list, nodes, body)
for el in anchors:
    print(f"  <{el['tag']}> attrs={el['attributes']}")
    print(f"  HTML → {el['html'][:120]!r}")
    print()

# ── Query by CLASS ────────────────────────────────────────────────────────────
# Change "some-class" to any class that appears on the page you're crawling
print("=" * 60)
print("get_by_class('some-class')")
print("=" * 60)
by_class = get_by_class("some-class", node_list, nodes, body)
if by_class:
    for el in by_class:
        print(f"  <{el['tag']}> attrs={el['attributes']}")
        print(f"  HTML → {el['html'][:120]!r}")
        print()
else:
    print("  (no elements matched — update the class name above)\n")

# ── Query by ID ───────────────────────────────────────────────────────────────
# Change "some-id" to any id that appears on the page you're crawling
print("=" * 60)
print("get_by_id('some-id')")
print("=" * 60)
by_id = get_by_id("some-id", node_list, nodes, body)
if by_id:
    print(f"  <{by_id['tag']}> attrs={by_id['attributes']}")
    print(f"  HTML → {by_id['html'][:120]!r}")
else:
    print("  (no element matched — update the id above)\n")
