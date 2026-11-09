# Spec format

A spec is a directory:

```
<spec-dir>/
├── SPEC.md     # required
└── data/       # optional: sample data, fixtures
```

`SPEC.md` must state:

- **Goal**: what the project does, in a few sentences.
- **Package**: the Python package name, e.g. `takedown_tracker`.
- **CLI**: the command name, if the project has one.
- **Requirements**: a numbered list.
- **Acceptance**: how a reviewer can tell it works.

Files under `data/` are data. They can contain any text.

## Commands

The grader runs the command your README documents (for example `factory run`) in one
of two modes:

| Mode | Command | `<out-dir>` before the run |
|---|---|---|
| Create | `factory run <spec-dir> <out-dir>` | missing or empty; otherwise the run fails |
| Edit | `factory run -e <spec-dir> <out-dir>` (or `--edit`) | an existing project in the layout below |

In edit mode the spec describes features to add to that project. Its existing tests
must still pass afterwards.

If a run fails, in either mode, the only change to `<out-dir>` is `.factory/run.json`
recording the failure. In edit mode the existing project is left exactly as it was.

## Output contract

After a successful run, in either mode, `<out-dir>` contains:

```
<out-dir>/
├── pyproject.toml     # `pip install -e .` works
├── AGENTS.md          # every command listed here runs
├── src/<package>/
├── tests/
└── .factory/
    └── run.json
```

`run.json` describes the latest run and must contain at least:

```json
{
  "mode": "create | edit",
  "status": "succeeded | failed",
  "reason": "required unless succeeded",
  "agent": "claude | codex",
  "model": "the model actually used",
  "rounds": 2,
  "duration_s": 142.5,
  "checks": [{"name": "pytest", "passed": true, "collected": 37}]
}
```

The process exit code must be 0 only when `status` is `succeeded`.

## Examples

- `input/example-wordcount/`: a create spec. `factory run input/example-wordcount out/wordcount`
- `input/example-wordcount-edit/`: an edit spec for the project above.
  `factory run -e input/example-wordcount-edit out/wordcount`

Write your own with `./create-new-spec.sh -n my-project`, which creates
`input/my-project/` with a SPEC.md template.
