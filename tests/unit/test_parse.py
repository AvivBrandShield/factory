from factory.main import parse_files


def test_parse_single_file():
    text = "FILE: app.py\n```python\nprint('hi')\n```\n"
    assert parse_files(text) == {"app.py": "print('hi')\n"}


def test_parse_two_files():
    text = (
        "FILE: a.py\n```python\nA = 1\n```\n"
        "FILE: b.py\n```python\nB = 2\n```\n"
    )
    assert parse_files(text) == {"a.py": "A = 1\n", "b.py": "B = 2\n"}


def test_parse_file_containing_a_fence():
    readme = "# Demo\n\n```bash\npip install demo\n```\n"
    text = "FILE: README.md\n```markdown\n" + readme + "```\n"
    assert parse_files(text) == {"README.md": readme}
