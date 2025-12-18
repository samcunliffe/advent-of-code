# aoc

My [Advent of Code](https://adventofcode.com/) solutions.

🍦 I'm going for _nearly_  vanilla Python. Numpy is allowed; Pytest for TDD; and obviously, I'm using [`uv`](https://docs.astral.sh/uv/).

I might change my mind about the rules next year.

![aoc-logos](https://github.com/user-attachments/assets/6dd356e2-13cd-4ba9-9390-80391107c1d2)

## `uv`


Install everything:

```sh
uv sync
```

My solutions are:

```sh
uv run python 2025/<day>/*.py
```

Tests with:

```sh
uv run pytest
```

(I manually increment the version in `pyproject.toml` and the `pytest.testpaths` in the GitHub action each year).
