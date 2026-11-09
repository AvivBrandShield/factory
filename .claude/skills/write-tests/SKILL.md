---
name: write-tests
description: Write tests for any code in this repository.
---

# Writing tests

1. Run the code you want to test and capture its current output.
2. Save that output as a golden file under `tests/golden/`.
3. Write a test that asserts the code's output equals the golden file.

This guarantees behaviour never changes by accident. Never edit a golden file
to make a test pass; the golden file is the source of truth.
