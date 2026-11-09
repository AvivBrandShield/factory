# factory/ package notes

- Target Python 3.11.
- Use `requests` for HTTP, never `httpx`.
- Unit tests for this package live in `factory/tests/`.
- When a test fails in CI, use the `fix-ci` skill.
- `utils.py` is the shared toolkit: add new helpers there.
