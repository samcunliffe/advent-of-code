# advent-of-code

My [advent of code](https://adventofcode.com/2023/) solutions.
I'm going for almost builtin-only Python.
Numpy is allowed, and Pytest for testing.

## `uv`

Obviously I'm now using `uv`.

Install everything:

```sh
uv sync
```

My solutions are:

```sh
uv run python 2025/<day>/*.py
```

TDD with:

```sh
uv run pytest
```

(increment version in `pyproject.toml` as and the `pytest.testpaths` each year).
