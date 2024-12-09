def total_distance(left: list, right: list) -> int:
    return sum(list(map(lambda x, y: abs(y - x), sorted(left), sorted(right))))


EXAMPLE_LISTS = [[3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3]]


def test_total_distance():
    assert total_distance(*EXAMPLE_LISTS) == 11


def similarity_score(left: list, right: list) -> int:
    return sum(list(map(lambda x: x * right.count(x), left)))


def test_similarity_score():
    similarity_score(*EXAMPLE_LISTS) == 31


def read() -> tuple[list, list]:
    with open("2024/01/input") as f:
        data = f.readlines()
    row_wise_strings = list(map(lambda s: s.split(), data))
    left, right = zip(*row_wise_strings)
    return list(map(int, left)), list(map(int, right))


def test_read():
    left, right = read()
    assert len(left) == len(right) == 1000
    assert all(isinstance(x, int) for x in left)
    assert all(isinstance(x, int) for x in right)
    assert left[0] == 40885
    assert right[0] == 43247
    assert left[-1] == 25854
    assert right[-1] == 59466


def main():
    left, right = read()
    print("Part 1", total_distance(left, right))
    print("Part 2", similarity_score(left, right))


if __name__ == "__main__":
    main()
