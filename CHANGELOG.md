# Change Logs

### Version 0.0.1

- Socket handling working great
- Almost clear response structure - header, body

### Version 0.0.2

- The response structure is clear, status, version, header and body is seperated
- Lexer working and outputting a token stream according to the grammar

### Version 0.1.0

- Minor/toy version done.
- Clear parsing ( tag soups handled )
- Fully traversable structure

### Version 0.1.1

- Adding extractors for tag, class and id
- Use main for user interaction instead of hardcoding. ( comments provided for understanding )

### Version 0.2.0

- Introduced OOP DOM layer (`src/dom/`)
- `HTMLElement` class: wraps a single parsed node, exposes `.tag`, `.attributes`, `.html`, `.text`, `.parent`, `.children`
- `HTMLDocument` class: builds the full element tree from lexer/parser output via a two-pass algorithm
- All three selectors (`get_by_tag`, `get_by_class`, `get_by_id`) available both at document level and scoped to any element (chainable queries)
- `src/query.py` retained for backward compatibility
- `main.py` updated to demonstrate the new API

### Version 0.3.0

- **HTTPClient** (`greenink.http.client`): raw TCP socket client with timeout support, handles `Content-Length` and `Transfer-Encoding: chunked` responses
- **HTTPResponse** (`greenink.http.client`): typed wrapper — `.status_code`, `.headers`, `.body`
- **HTMLParser** (`greenink.parser`): single-call facade — `HTMLParser.parse(html)` → `HTMLDocument`
- **Package rename**: `src/` → `greenink/` for clean PyPI distribution
- **`greenink/__init__.py`**: top-level public API — all classes importable from `greenink` directly
- **`pyproject.toml`**: setuptools build config for PyPI (`greenink-scraper`)
- **GitHub Actions**: `.github/workflows/publish.yml` — auto-publishes to PyPI on `v*.*.*` tag via OIDC trusted publishing
- **`main.py`**: reduced to 3-line setup using the clean public API

### Version 0.3.1

- **Branding rename**: package renamed from `greenink` → `faircrawler` (company name removed)
- PyPI package name updated to `fair-crawler`
- Importable as `from faircrawler import HTTPClient, HTMLParser, HTMLDocument, HTMLElement`

### Version 0.4.0

- **HTTPS support**: `HTTPClient` now wraps the TCP socket with `ssl.create_default_context()` automatically for `https://` URLs
- **`URL` class** (`faircrawler.http.url`): parses any URL string into `.scheme`, `.host`, `.port`, `.path`, `.is_secure`; resolves relative redirect locations
- **Redirect following**: `HTTPClient` auto-follows 301/302/303/307/308 with configurable `max_redirects=5`
- **`verify_ssl=True`** param on `HTTPClient` — set `False` for self-signed certificates
- **Exception hierarchy** (`faircrawler.http.exceptions`): `FairCrawlerError`, `TooManyRedirectsError`, `SSLVerificationError`, `ConnectionError`
- **`HTTPResponse.ok`**: `True` if status is 2xx
- **`HTTPResponse.url`**: the final URL after all redirects