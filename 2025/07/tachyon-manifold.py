EXAMPLE = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


def find_entrance(first_row):
    return {first_row.index("S")}


def test_find_entrance():
    expected = {7}
    obtained = find_entrance(EXAMPLE.strip().splitlines()[0])
    assert expected == obtained


def process_row(row, entrance_positions):
    splitters = [p for p in entrance_positions if row[p] == "^"]
    new = set(p for p in entrance_positions if row[p] == ".")
    new = new.union(p - 1 for p in splitters)
    new = new.union(p + 1 for p in splitters)
    return new, len(splitters)


def test_process_row():
    expected_new_sources = {7}
    expected_splits = 0
    obtained_new_sources, obtained_splits = process_row("...............", {7})
    assert expected_new_sources == obtained_new_sources
    assert expected_splits == obtained_splits

    expected_new_sources = {6, 8}
    expected_splits = 1
    obtained_new_sources, obtained_splits = process_row(".......^.......", {7})
    assert expected_new_sources == obtained_new_sources
    assert expected_splits == obtained_splits


def process_tachyon_manifold(manifold):
    splits = 0
    start = find_entrance(manifold[0])
    for row in manifold[1:]:
        start, splits_this_row = process_row(row, start)
        splits += splits_this_row
    return splits


def test_process_tachyon_manifold():
    expected = 21
    obtained = process_tachyon_manifold(EXAMPLE.splitlines())
    assert expected == obtained


if __name__ == "__main__":
    with open("2025/07/input") as f:
        print(process_tachyon_manifold(f.readlines()))
