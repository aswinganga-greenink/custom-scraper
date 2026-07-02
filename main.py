from faircrawler import HTTPClient, HTMLParser

# ── Configure ─────────────────────────────────────────────────────────────────
domain = "neverssl.com"
client = HTTPClient(timeout=10)

# ── Fetch & parse ─────────────────────────────────────────────────────────────
response = client.get(domain)
print(response)

doc = HTMLParser.parse(response.body)
print(doc)

# ── Query ─────────────────────────────────────────────────────────────────────
print("\n── All <a> tags ──")
for link in doc.get_by_tag("a"):
    print(f"  {link.text!r:30s} → {link.attributes.get('href', '(no href)')}")

print("\n── Scoped: <body> → <a> ──")
body_el = doc.get_by_tag("body")
if body_el:
    for link in body_el[0].get_by_tag("a"):
        print(f"  {link}")
