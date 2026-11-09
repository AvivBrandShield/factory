# Factory architecture

The factory has three stages that run in parallel.

1. **Planner.** Reads `SPEC.md`, writes `plan.json` with one task per file,
   and asks clarifying questions through Slack.
2. **Workers.** A pool of 8 workers, one coding agent each, builds the files
   in the plan. Each worker runs in its own git worktree.
3. **Verifier.** Runs the generated project's test suite with coverage and
   rejects any project below 90%. Failures go back to the worker with the
   full log, for at most 3 rounds.

Results are written to `out/<name>/` together with `report.html`.

The planner, workers and verifier communicate through Redis.
