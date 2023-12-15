import re


def is_symbol(ch):
    return ch in "$*+#/-=@%&"


def grid(data):
    return [line.strip() for line in data.splitlines() if line != ""]


def test_parse_grid():
    test_data = """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598.."""
    g = grid(test_data)
    assert len(g) == 10
    assert len(g[0]) == 10


def adjacent_coordinates(row, col_start, col_end, size):
    return [
        (r, c)
        for r in (row - 1, row, row + 1)
        for c in range(col_start - 1, col_end + 1)
        if 0 <= r < size and 0 <= c < size
    ]


def test_adjacency():
    expected = [(0, 0), (0, 1), (0, 2), (0, 3),
                (1, 0), (1, 1), (1, 2), (1, 3)]  # fmt: skip
    obtained = adjacent_coordinates(0, 0, 3, 10)
    assert sorted(expected) == sorted(obtained)


def process(grid):
    total = 0
    for row_number, row in enumerate(grid):
        for part_candidate in re.finditer(r"\d+", row):
            coordinates = adjacent_coordinates(
                row_number, part_candidate.start(), part_candidate.end(), len(grid)
            )
            for r, c in coordinates:
                if is_symbol(grid[r][c]):
                    total += int(part_candidate.group())
                    break
                    # nesting 🤮
    return total


def test_full_process():
    test_data = """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598.."""
    assert process(grid(test_data)) == 4361


with open("2023/3/input.txt") as f:
    print(process(grid(f.read())))
