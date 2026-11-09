#!/usr/bin/env bash
# Create a new spec folder under input/ with a SPEC.md template.
set -euo pipefail

usage() {
  cat <<EOF
Usage: $(basename "$0") -n <name>

Create input/<name>/ with a SPEC.md template and an empty data/ folder.

Options:
  -n <name>   spec name: lowercase letters, digits and dashes (e.g. my-project)
  -h          show this help
EOF
}

name=""
while getopts ":n:h" opt; do
  case "$opt" in
    n) name="$OPTARG" ;;
    h) usage; exit 0 ;;
    :) echo "error: -$OPTARG needs a value" >&2; usage >&2; exit 2 ;;
    *) echo "error: unknown option -$OPTARG" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ -z "$name" ]]; then
  echo "error: -n <name> is required" >&2
  usage >&2
  exit 2
fi

if [[ ! "$name" =~ ^[a-z][a-z0-9-]*$ ]]; then
  echo "error: '$name' is not a valid name: use lowercase letters, digits and dashes, starting with a letter" >&2
  exit 2
fi

spec_dir="$(cd "$(dirname "$0")" && pwd)/input/$name"
if [[ -e "$spec_dir" ]]; then
  echo "error: $spec_dir already exists" >&2
  exit 1
fi

package="${name//-/_}"
mkdir -p "$spec_dir/data"
cat > "$spec_dir/SPEC.md" <<EOF
# $name

## Goal

What the project does, in a few sentences.

## Package

\`$package\`

## CLI

\`$name\` (delete this section if the project has no CLI)

## Requirements

1. ...
2. ...

## Acceptance

How a reviewer can tell it works.
EOF

echo "Created $spec_dir"
echo "Next: fill in $spec_dir/SPEC.md and put any sample data in $spec_dir/data/"
