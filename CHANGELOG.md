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