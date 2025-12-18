import pytest
import numpy
from numpy.testing import assert_array_equal

EXAMPLE = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def array_example():
    return numpy.array([list(row) for row in EXAMPLE.strip().split("\n")])


def test_array_example():
    expected_first_row = numpy.array([".", ".", "@", "@", ".", "@", "@", "@", "@", "."])
    obtained = array_example()
    assert_array_equal(obtained[0], expected_first_row)
    assert obtained.shape == (10, 10)


def _roll_to_int(s):
    return 1 if s == "@" else 0


def roll_to_int(s_array):
    return numpy.vectorize(_roll_to_int)(s_array)


def test_roll_to_int():
    assert _roll_to_int("@") == 1
    assert _roll_to_int(".") == 0

    expected_first_row = numpy.array([0, 0, 1, 1, 0, 1, 1, 1, 1, 0])
    first_row = array_example()[0]
    obtained = roll_to_int(first_row)
    assert_array_equal(obtained, expected_first_row)


def get_puzzle_input(path="2025/04/input"):
    with open(path) as f:
        grid = numpy.array([list(line.strip()) for line in f if line.strip()])
    return roll_to_int(grid)


def neighbour_coordinates(x, y, grid_shape):
    """Get the 8 neighbouring coordinates of (x, y) bounded within the grid shape."""
    # (-1, -1)  (-1, 0)  (-1, 1)
    # ( 0, -1)     *     ( 0, 1)
    # ( 1, -1)  ( 1, 0)  ( 1, 1)
    x_max, y_max = grid_shape
    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < x_max and 0 <= ny < y_max:
            yield nx, ny


def test_neighbours():
    grid = array_example()
    # (0, 0)  (0, 1)  (0, 2)
    # (1, 0) *(1, 1)* (1, 2)
    # (2, 0)  (2, 1)  (2, 2)
    x, y = 1, 1
    obtained = list(neighbour_coordinates(x, y, grid.shape))
    expected = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    assert obtained == expected

    # Corner should crop...
    # *(0, 0)* (0, 1)
    #  (1, 0)  (1, 1)
    x, y = 0, 0
    obtained = list(neighbour_coordinates(x, y, grid.shape))
    expected = [(0, 1), (1, 0), (1, 1)]
    assert obtained == expected


def can_be_accessed_by_forklift(x, y, grid):
    neighbours = neighbour_coordinates(x, y, grid.shape)
    return 4 > sum(grid[nx, ny] for nx, ny in neighbours)


def test_can_be_accessed_by_forklift():
    # From the worked example:
    # ..xx.xx@x.   (row 0)
    # x@@.@.@.@@   (row 1)
    # (rest of the grid omitted)
    #
    # Where x can be accessed, @ cannot, and . is an empty space.
    grid = roll_to_int(array_example())

    # Position (0, 2) can be accessed (3 occupied neighbours)
    assert can_be_accessed_by_forklift(0, 2, grid)

    # Position (0, 7) cannot be accessed (4 occupied neighbours)
    assert not can_be_accessed_by_forklift(0, 7, grid)


def _count(x, y, grid):
    is_occupied_by_roll = grid[x, y] == 1
    return 1 if is_occupied_by_roll and can_be_accessed_by_forklift(x, y, grid) else 0


def count_accessible_positions(grid):
    count = 0
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            count += _count(x, y, grid)

    return count


def test_example():
    grid = roll_to_int(array_example())
    obtained = count_accessible_positions(grid)
    expected = 13
    assert obtained == expected


if __name__ == "__main__":
    print(count_accessible_positions(get_puzzle_input()))
