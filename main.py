from greenink.tcpConn import create_connection, get_http_response
from greenink.lexer import lexer, attr_tokenizer
from greenink.htmlParser import html_parser
from greenink.dom import HTMLDocument

domain = "neverssl.com"

# ── Fetch ─────────────────────────────────────────────────────────────────────
fd       = create_connection(domain)
response = get_http_response(fd, domain)
body     = response["body"]

# ── Parse into token list + node tree ────────────────────────────────────────
node_list = lexer(body)
node_list = attr_tokenizer(node_list)
nodes     = html_parser(node_list)

# ── Build the HTMLDocument ────────────────────────────────────────────────────
doc = HTMLDocument(node_list, nodes, body)
print(doc)

# ── Document-level queries ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("doc.get_by_tag('a')")
print("=" * 60)
for link in doc.get_by_tag("a"):
    href = link.attributes.get("href", "(no href)")
    print(f"  {link}")
    print(f"  href  = {href}")
    print(f"  text  = {link.text!r}")
    print(f"  html  = {link.html[:100]!r}")
    print()

# ── Scoped / chained query ────────────────────────────────────────────────────
# Find the <body> element, then search only inside it.
print("=" * 60)
print("doc.get_by_tag('body')[0].get_by_tag('a')  ← scoped search")
print("=" * 60)
body_els = doc.get_by_tag("body")
if body_els:
    for link in body_els[0].get_by_tag("a"):
        print(f"  {link}  →  {link.attributes.get('href', '')}")
else:
    print("  (no <body> found)")

# ── Query by class & id (update values to match the target page) ──────────────
print("\n" + "=" * 60)
print("doc.get_by_class('some-class')")
print("=" * 60)
by_class = doc.get_by_class("some-class")
if by_class:
    for el in by_class:
        print(f"  {el}")
else:
    print("  (no match — update the class name above)")

print("\n" + "=" * 60)
print("doc.get_by_id('some-id')")
print("=" * 60)
by_id = doc.get_by_id("some-id")
if by_id:
    print(f"  {by_id}")
    print(f"  html = {by_id.html[:120]!r}")
else:
    print("  (no match — update the id above)")
