from numpy import prod


bag_contents = {"red": 12, "green": 13, "blue": 14}


def less_than_in_bag(draw):
    counts_this_turn = draw.split(",")
    for count in counts_this_turn:
        number_drawn, colour = count.strip().split(" ")
        if int(number_drawn) > bag_contents[colour]:
            return False
    return True


def parse_game(game):
    game_id, all_turns = game.split(":")
    id = int(game_id.split(" ")[1])
    turns = all_turns.split(";")
    return id, turns


def turns_are_possible(turns):
    return all([less_than_in_bag(draw) for draw in turns])


def test_turns_are_possible():
    assert turns_are_possible(["3 blue, 4 red", "1 red, 2 green, 6 blue", "2 green"]) is True  # fmt: skip
    assert turns_are_possible(["8 green, 6 blue, 20 red", "5 blue, 4 red, 13 green", "5 green, 1 red"]) is False  # fmt: skip


def id_if_game_is_possible(game):
    id, turns = parse_game(game)
    if turns_are_possible(turns):
        return id
    return 0


with open("2023/2/input.txt") as fi:
    answer_part_1 = sum([id_if_game_is_possible(game) for game in fi])
    print(answer_part_1)


def minimal_bag_contents(turns):
    bag = {"red": 0, "green": 0, "blue": 0}
    for draw in turns:
        for balls in draw.split(","):
            number_drawn, colour = balls.strip().split(" ")
            bag[colour] = max(bag[colour], int(number_drawn))
    return bag


def test_minimal_bag_contents():
    assert minimal_bag_contents(["3 blue, 4 red", "1 red, 2 green, 6 blue", "2 green"]) == {"red": 4, "green": 2, "blue": 6}  # fmt: skip
    assert minimal_bag_contents(["1 blue, 2 green", "3 green, 4 blue, 1 red", "1 green, 1 blue"]) == {"red": 1, "green": 3, "blue": 4}  # fmt: skip


def power(bag):
    return prod(list(bag.values()))


def test_power():
    assert power({"red": 4, "green": 2, "blue": 6}) == 48


def power_of_minimal_bag(game):
    _, turns = parse_game(game)
    return power(minimal_bag_contents(turns))


with open("2023/2/input.txt") as fi:
    answer_part_2 = sum([power_of_minimal_bag(game) for game in fi])
    print(answer_part_2)
