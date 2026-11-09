# wordcount: top words

An edit spec: run it with `-e` against a project built from `input/example-wordcount`.

## Goal

Add a report of the most frequent words to the existing `wordcount` tool.

## Package

`wordcount` (existing)

## CLI

`wordcount` (existing)

## Requirements

1. `wordcount --top N FILE [FILE ...]` prints the N most frequent words across all
   files, one per line as `<count> <word>`, most frequent first.
2. Words are compared case-insensitively and printed in lower case. Leading and
   trailing punctuation is stripped (`dog.` counts as `dog`).
3. Ties are broken alphabetically.
4. With `--json`, `--top` prints `[{"word": ..., "count": ...}]` instead.
5. Everything the tool did before keeps working unchanged.

## Acceptance

- `wordcount --top 2 data/sample.txt` prints `3 the` then `1 again`.
- The project's existing tests still pass.
