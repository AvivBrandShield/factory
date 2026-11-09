# Software Factory

Give it a spec, get a working project. The factory uses your AI coding agent
(Claude Code or Codex) to plan, build and verify a complete Python project.

## Quickstart

```bash
pip install -r requirements.txt
./create-new-spec.sh -n my-spec      # then fill in input/my-spec/SPEC.md
python -m factory.main input/my-spec out/my-spec
```

You will be asked which coding agent you use.

## Architecture

The factory runs a planner, a pool of workers and a verifier. See
[docs/architecture.md](docs/architecture.md).

## Tests

```bash
pytest tests/unit -k "not slow" -q
```

All tests pass on main.
