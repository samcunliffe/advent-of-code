import pytest


def parse(report: str) -> list:
    return [int(x) for x in report.split()]


def test_parse():
    assert parse("7 6 4 2 1") == [7, 6, 4, 2, 1]


def in_order(report: list) -> bool:
    return report == sorted(report) or report == sorted(report, reverse=True)


def test_ordering():
    assert in_order([1, 2, 3, 4, 5])
    assert not in_order([2, 1, 3, 4, 5])


def correctly_spaced(report: list[int], acceptable_gaps=[1, 2, 3]) -> bool:
    return all(
        abs(report[i] - report[i + 1]) in acceptable_gaps
        for i in range(len(report) - 1)
    )


def test_spacing():
    assert not correctly_spaced([1, 1])
    assert correctly_spaced([1, 2])
    assert correctly_spaced([1, 3])
    assert correctly_spaced([1, 4])
    assert not correctly_spaced([1, 5])
    assert not correctly_spaced([1, 6])
    assert not correctly_spaced([1, 1000])


def is_safe(report: str) -> bool:
    return in_order(parse(report)) and correctly_spaced(parse(report))


@pytest.mark.parametrize(
    "report, expected_safe",
    [
        ("7 6 4 2 1", True),
        ("1 3 6 7 9", True),
        ("1 2 7 8 9", False),
        ("9 7 6 2 1", False),
        ("1 3 2 4 5", False),
        ("8 6 4 4 1", False),
    ],
)
def test_safe(report, expected_safe):
    assert is_safe(report) == expected_safe


def read() -> list[str]:
    with open("2024/02/input") as f:
        return f.readlines()


def main():
    reports = read()
    print(sum(is_safe(report) for report in reports))


if __name__ == "__main__":
    main()
