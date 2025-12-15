import pytest


EXAMPLE = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"


def parse(range_):
    start, end = range_.split("-")
    return int(start), int(end)


@pytest.mark.parametrize(
    "range_,expected",
    [
        ("11-22", (11, 22)),
        ("998-1012", (998, 1012)),
    ],
)
def test_parse(range_, expected):
    obtained = parse(range_)
    assert obtained == expected


def valid(id):
    sid = str(id)
    odd_length = len(sid) % 2 != 0
    if odd_length:
        return True

    mid = len(sid) // 2
    first_half = sid[:mid]
    second_half = sid[mid:]
    return first_half != second_half


@pytest.mark.parametrize(
    "id,expected",
    [
        (22, False),
        (11, False),
        (1010, False),
        (6464, False),
        (123123, False),
        (101, True),
        (1188511885, False),
        (222222, False),
        (1, True),
    ],
)
def test_valid(id, expected):
    obtained = valid(id)
    assert obtained == expected


def sum_invalid(range_):
    start, end = parse(range_)
    return sum(id for id in range(start, end + 1) if not valid(id))


@pytest.mark.parametrize(
    "range_,expected",
    [
        ("11-22", 11 + 22),
        ("95-115", 99),
        ("998-1012", 1010),
        ("1188511880-1188511890", 1188511885),
        ("222220-222224", 222222),
        ("1698522-1698528", 0),
    ],
)
def test_count_invalid(range_, expected):
    obtained = sum_invalid(range_)
    assert obtained == expected


def sum_invalid_ids(ranges):
    return sum(sum_invalid(r) for r in ranges)


def test_example():
    ranges = EXAMPLE.split(",")
    obtained = sum_invalid_ids(ranges)
    assert obtained == 1227775554


if __name__ == "__main__":
    with open("2025/02/input") as f:
        ranges = f.read().split(",")
    print(sum_invalid_ids(ranges))
