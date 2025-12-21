import pytest
import numpy
from numpy.testing import assert_array_equal

EXAMPLE = """
123 328   51  64
 45  64  387  23
  6  98  215 314
  *   +   *   +
"""


def process_line(line):
    tokens = line.split(" ")
    return [token.strip() for token in tokens if token.strip() != ""]


def test_process_line():
    expected = ["45", "64", "387", "23"]
    obtained = process_line(" 45  64  387  23\n")
    assert expected == obtained


def parse_grid(s):
    return numpy.array([process_line(line) for line in s.strip().splitlines()])


def test_parse_grid():
    expected = numpy.array(
        [
            ["123", "328", "51", "64"],
            ["45", "64", "387", "23"],
            ["6", "98", "215", "314"],
            ["*", "+", "*", "+"],
        ]
    )
    obtained = parse_grid(EXAMPLE)
    assert_array_equal(obtained, expected)


def numpy_operator(op):
    if op == "+":
        return numpy.sum
    elif op == "*":
        return numpy.prod
    else:
        raise ValueError(f"Unknown operation: {op}")


def test_numpy_operator():
    assert numpy_operator("+") == numpy.sum
    assert numpy_operator("*") == numpy.prod
    with pytest.raises(ValueError):
        numpy_operator("-")


def process_column(col):
    op = numpy_operator(col[-1])
    return op(numpy.vectorize(int)(col[:-1]))


@pytest.mark.parametrize(
    "test_column, expected",
    [
        (numpy.array(["123", "45", "6", "*"]), 33210),
        (numpy.array(["328", "64", "98", "+"]), 490),
    ],
)
def test_process_column(test_column, expected):
    obtained = process_column(test_column)
    assert obtained == expected


def do_homework(grid):
    return sum(process_column(col) for col in grid.transpose())


def test_do_homework():
    grid = parse_grid(EXAMPLE)
    assert do_homework(grid) == 4277556


if __name__ == "__main__":
    with open("2025/06/input") as f:
        lines = f.read()
    print(do_homework(parse_grid(lines)))
