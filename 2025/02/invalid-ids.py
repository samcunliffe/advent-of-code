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


def sum_invalid(range_, check=valid):
    start, end = parse(range_)
    return sum(id for id in range(start, end + 1) if not check(id))


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
def test_sum_invalid(range_, expected):
    obtained = sum_invalid(range_)
    assert obtained == expected


def sum_invalid_ids(ranges, check=valid):
    return sum(sum_invalid(r, check) for r in ranges)


def test_example():
    ranges = EXAMPLE.split(",")
    obtained = sum_invalid_ids(ranges)
    assert obtained == 1227775554


def is_divisor(n, d):
    return n % d == 0


def divisors(n):
    for d in range(n + 1, 1, -1):
        if is_divisor(n, d):
            yield d


@pytest.mark.parametrize(
    "n,expected",
    [
        (1, []),
        (2, [2]),
        (3, [3]),
        (4, [4, 2]),
        (6, [6, 3, 2]),
        (12, [12, 6, 4, 3, 2]),
    ],
)
def test_divisors(n, expected):
    obtained = list(divisors(n))
    assert obtained == expected


def strlen(i):
    return str(i), len(str(i))


def valid2(id):
    s, n = strlen(id)

    for divisor in divisors(n):
        chunk = n // divisor
        parts = [s[i * chunk : (i + 1) * chunk] for i in range(divisor)]

        if all(part == parts[0] for part in parts):
            return False

    return True


@pytest.mark.parametrize(
    "id,expected",
    [
        (12341234, False),
        (123123123, False),
        (1212121212, False),
        (1111111, False),
        (1, True),
        (10, True),
        (100, True),
        (1000, True),
        (121, True),
        (123321, True),
        (1231234, True),
        (4242424243, True),
    ],
)
def test_valid2(id, expected):
    obtained = valid2(id)
    assert obtained == expected


@pytest.mark.parametrize(
    "range_,expected",
    [
        ("11-22", 11 + 22),
        ("95-115", 99 + 111),
        ("998-1012", 999 + 1010),
        ("1188511880-1188511890", 1188511885),
        ("222220-222224", 222222),
        ("1698522-1698528", 0),
        ("824824821-824824827", 824824824),
        ("2121212118-2121212124", 2121212121),
    ],
)
def test_sum_invalid2(range_, expected):
    obtained = sum_invalid(range_, valid2)
    assert obtained == expected


def test_example2():
    ranges = EXAMPLE.split(",")
    obtained = sum_invalid_ids(ranges, valid2)
    assert obtained == 4174379265


if __name__ == "__main__":
    with open("2025/02/input") as f:
        ranges = f.read().split(",")
    print(sum_invalid_ids(ranges))
    print(sum_invalid_ids(ranges, valid2))
