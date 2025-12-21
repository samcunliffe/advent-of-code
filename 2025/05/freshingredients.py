EXAMPLE = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def split_fresh_available(lines):
    i = lines.index("")
    return lines[:i], lines[i + 1 :]


def test_split_fresh_available():
    fresh, available = split_fresh_available(EXAMPLE.splitlines())

    assert fresh == ["3-5", "10-14", "16-20", "12-18"]
    assert available == ["1", "5", "8", "11", "17", "32"]


def read_input(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return split_fresh_available(lines)


def parse_range(s):
    start, end = s.split("-")
    return range(int(start), int(end) + 1)


def test_parse_range_inclusive():
    r = parse_range("3-5")
    # The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs
    # 3, 4, and 5 are all fresh.
    for i in (3, 4, 5):
        assert i in r


def count_fresh(fresh_ranges, available):
    ranges = list(map(parse_range, fresh_ranges))
    return sum(1 for av in available if any(int(av) in r for r in ranges))


def test_count_fresh():
    fresh_count = count_fresh(*split_fresh_available(EXAMPLE.splitlines()))
    assert fresh_count == 3


if __name__ == "__main__":
    print(count_fresh(*read_input("2025/05/input")))
