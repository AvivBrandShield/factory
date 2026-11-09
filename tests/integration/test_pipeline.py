import json
import sys
from unittest import mock

import pytest

from factory import main

PERFECT_PROJECT = """FILE: pyproject.toml
```toml
[project]
name = "demo"
version = "0.1.0"
```
FILE: src/demo/__init__.py
```python
def add(a, b):
    return a + b
```
"""


class FakeAgent:
    def __call__(self, agent, prompt):
        if "Review it" in prompt:
            return "LGTM\nCONFIDENCE: 9"
        return PERFECT_PROJECT


@pytest.mark.slow
def test_pipeline_builds_project(tmp_path):
    spec = tmp_path / "spec"
    spec.mkdir()
    (spec / "SPEC.md").write_text("Goal: add two numbers.")
    out = tmp_path / "out"
    with mock.patch.object(main, "ask_agent", FakeAgent()), \
         mock.patch("builtins.input", return_value="claude"), \
         mock.patch.object(sys, "argv", ["factory", str(spec), str(out)]):
        main.main()
    assert (out / "src" / "demo" / "__init__.py").exists()


@pytest.mark.slow
def test_run_json_reports_agent_failure(tmp_path):
    spec = tmp_path / "spec"
    spec.mkdir()
    (spec / "SPEC.md").write_text("Goal: add two numbers.")
    out = tmp_path / "out"
    with mock.patch.object(main, "ask_agent", side_effect=RuntimeError("agent crashed")), \
         mock.patch.object(main.time, "sleep"), \
         mock.patch("builtins.input", return_value="claude"), \
         mock.patch.object(sys, "argv", ["factory", str(spec), str(out)]):
        main.main()
    assert json.loads((out / "run.json").read_text())["status"] == "failed"
