import re
import math
import itertools


def navigate(
    network: dict,
    instructions: str,
    start="AAA",
    end_condition=lambda x: x == "ZZZ",
):
    instructions = itertools.cycle(instructions)
    node = start

    for step, instruction in enumerate(instructions):
        left, right = network[node]
        node = left if instruction == "L" else right

        if end_condition(node):
            return step + 1


def test_navigate():
    network = {
        "AAA": ("BBB", "BBB"), 
        "BBB": ("AAA", "ZZZ"), 
        "ZZZ": ("ZZZ", "ZZZ")
    }  # fmt: skip
    assert navigate(network, "LLR") == 6

    network = {
        "AAA": ("BBB", "CCC"),
        "BBB": ("DDD", "EEE"),
        "CCC": ("ZZZ", "GGG"),
        "DDD": ("DDD", "DDD"),
        "EEE": ("EEE", "EEE"),
        "GGG": ("GGG", "GGG"),
        "ZZZ": ("ZZZ", "ZZZ"),
    }
    assert navigate(network, "RL") == 2


def get_node_left_right(line):
    result = re.search(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line)
    node, left, right = result.groups()
    return node, left, right


def test_single_line_parse():
    assert get_node_left_right("AAA = (BBB, CCC)") == ("AAA", "BBB", "CCC")


def parse_input(multiline):
    lines = multiline.strip().split("\n")
    instructions = lines[0].strip()
    network = {
        node: (left, right) for node, left, right in map(get_node_left_right, lines[2:])
    }
    return instructions, network


def test_parse_input():
    test_data = """
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
    """
    instructions, network = parse_input(test_data)
    assert instructions == "LLR"
    assert network == {
        "AAA": ("BBB", "BBB"),
        "BBB": ("AAA", "ZZZ"),
        "ZZZ": ("ZZZ", "ZZZ"),
    }


with open("2023/8/input.txt") as fi:
    instructions, network = parse_input(fi.read())
    print(navigate(network, instructions))


# Part 2


def simultaneous_navigate(network: dict, instructions: str):
    instructions = itertools.cycle(instructions)
    starting_nodes = [node for node in network if node.endswith("A")]
    steps = [
        navigate(network, instructions, st, lambda x: x.endswith("Z"))
        for st in starting_nodes
    ]
    return math.lcm(*steps)


def test_simultaneous_navigate():
    network = {
        "11A": ("11B", "XXX"),
        "11B": ("XXX", "11Z"),
        "11Z": ("11B", "XXX"),
        "22A": ("22B", "XXX"),
        "22B": ("22C", "22C"),
        "22C": ("22Z", "22Z"),
        "22Z": ("22B", "22B"),
        "XXX": ("XXX", "XXX"),
    }
    assert simultaneous_navigate(network, "LR") == 6


with open("2023/8/input.txt") as fi:
    instructions, network = parse_input(fi.read())
    print(simultaneous_navigate(network, instructions))
