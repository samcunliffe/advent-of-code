import time
from numpy import prod


def distances_possible(race_time):
    distances = []
    for button_press in range(1, race_time):
        sailing_time = race_time - button_press
        speed = button_press
        distances += [speed * sailing_time]
    return distances


def test_distances_possible():
    assert distances_possible(7) == [6, 10, 12, 12, 10, 6]


def number_ways_to_win(race_time, distance):
    return len(list(filter(lambda d: d > distance, distances_possible(race_time))))


def test_number_ways_to_win():
    assert number_ways_to_win(7, 9) == 4
    assert number_ways_to_win(15, 40) == 8
    assert number_ways_to_win(30, 200) == 9


def parse_input(multiline):
    lines = multiline.strip().split("\n")
    race_times_ms = [int(t) for t in lines[0].split()[1:]]
    records_mm = [int(d) for d in lines[1].split()[1:]]
    return zip(race_times_ms, records_mm)


with open("2023/6/input.txt") as fi:
    answer_part_1 = prod([number_ways_to_win(r, d) for r, d in parse_input(fi.read())])
    print(answer_part_1)


def test_new_way():
    assert number_ways_to_win(71530, 940200) == 71503


def new_way_to_parse_input(multiline):
    lines = multiline.strip().split("\n")
    race_time_ms = int("".join(lines[0].split()[1:]))
    records_mm = int("".join(lines[1].split()[1:]))
    return race_time_ms, records_mm


with open("2023/6/input.txt") as fi:
    start = time.time()
    answer_part_2 = number_ways_to_win(*new_way_to_parse_input(fi.read()))
    time_taken = time.time() - start

    print(answer_part_2)
    print(f"time for part 2: {time_taken:.2f} sec")
