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


def parse_ranges(l):
    return list(map(parse_range, l))


def count_fresh_available(fresh_ranges, available):
    ranges = parse_ranges(fresh_ranges)
    return sum(1 for av in available if any(int(av) in r for r in ranges))


def test_count_fresh():
    fresh_count = count_fresh_available(*split_fresh_available(EXAMPLE.splitlines()))
    assert fresh_count == 3


def test_dont_ruin_first_answer():
    assert count_fresh_available(*read_input("2025/05/input")) == 720


def max_fresh(fresh_ranges):
    ranges = parse_ranges(fresh_ranges)
    return max(r.stop - 1 for r in ranges)


def test_max_fresh():
    fresh_ranges, _ = split_fresh_available(EXAMPLE.splitlines())
    assert max_fresh(fresh_ranges) == 20


def count_fresh_in_range(fresh_ranges):
    max = max_fresh(fresh_ranges)
    return sum(
        1 for i in range(max + 1) if any(i in r for r in parse_ranges(fresh_ranges))
    )


def test_count_fresh_in_range():
    fresh_ranges, _ = split_fresh_available(EXAMPLE.splitlines())
    assert count_fresh_in_range(fresh_ranges) == 14


if __name__ == "__main__":
    print(count_fresh_available(*read_input("2025/05/input")))
    # print(count_fresh_in_range(read_input("2025/05/input")[0]))
