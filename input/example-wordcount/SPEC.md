# wordcount

## Goal

A small command-line tool that counts lines, words and characters in text files, like
a friendlier `wc`, with JSON output for scripts.

## Package

`wordcount`

## CLI

`wordcount`

## Requirements

1. `wordcount FILE [FILE ...]` prints one line per file: `<lines> <words> <chars> <path>`,
   then a `total` line when more than one file is given.
2. A word is a maximal run of non-whitespace characters. Characters are Unicode code
   points, not bytes. Lines are counted as text lines: a last line without a trailing
   newline still counts, and an empty file has 0 lines.
3. `--json` prints a JSON list instead: `[{"path": ..., "lines": ..., "words": ...,
   "chars": ...}]`, with no total entry.
4. `-` as a file name reads standard input.
5. A missing or unreadable file prints `wordcount: <path>: <reason>` to stderr, the
   other files are still counted, and the exit code is 1. Otherwise the exit code is 0.
6. Files are read as UTF-8; invalid bytes are replaced, never fatal.

## Acceptance

- `wordcount data/sample.txt` prints `3 12 61 data/sample.txt`.
- `printf 'a b\nc' | wordcount -` prints `2 3 5 -`.
- `wordcount --json data/sample.txt missing.txt` prints one JSON entry, an error on
  stderr, and exits 1.
