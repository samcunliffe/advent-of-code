import pytest


EXAMPLE = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


def cycle(start, stop, step, modulo=100):
    """A cyclical version of range."""
    i = start
    while i != stop:
        yield i
        i = (i + step) % modulo


@pytest.mark.parametrize(
    "start,stop,step,expected",
    [
        (98, 3, 1, [98, 99, 0, 1, 2]),
        (2, 98, -1, [2, 1, 0, 99]),
        (0, 0, 1, []),
    ],
)
def test_cycle_mod_100(start, stop, step, expected):
    obtained = cycle(start, stop, step)
    assert list(obtained) == expected


def parse(move):
    direction, nsteps = move[0], move[1:]

    if direction not in ("L", "R") or not nsteps.isdigit():
        raise ValueError("Invalid move")

    return direction, int(nsteps)


@pytest.mark.parametrize(
    "move,expected",
    [
        ("L68", ("L", 68)),
        ("R30", ("R", 30)),
        ("L0", ("L", 0)),
    ],
)
def test_parse(move, expected):
    obtained = parse(move)
    assert obtained == expected


@pytest.mark.parametrize(
    "move",
    [
        "X68",
        "L-30",
        "R3O",
        "68L",
    ],
)
def test_parse_raises(move):
    with pytest.raises(ValueError):
        parse(move)


def left_right_to_plus_minus(direction):
    if direction == "L":
        return -1
    return 1


@pytest.mark.parametrize(
    "direction,expected",
    [
        ("L", -1),
        ("R", 1),
    ],
)
def test_left_right_to_plus_minus(direction, expected):
    obtained = left_right_to_plus_minus(direction)
    assert obtained == expected


class Dial:
    def __init__(self):
        self.pointing_to = 50
        self.n_stops_at_zero = 0
        self.n_click_passes_zero = 0

    def move(self, move):
        direction, nsteps = parse(move)
        step = left_right_to_plus_minus(direction)
        stop = (self.pointing_to + step * nsteps) % 100
        ncycles = nsteps // 100
        self.n_click_passes_zero += ncycles

        if stop == 0:
            self.n_stops_at_zero += 1

        first_click = (self.pointing_to + step) % 100
        last_click = (stop + step) % 100
        # if 0 in cycle(first_click, last_click, step):
        if 0 in cycle(first_click, last_click, step):
            self.n_click_passes_zero += 1

        self.pointing_to = stop


def test_moves_example():
    d = Dial()
    d.move("L68")
    assert d.pointing_to == 82
    assert d.n_stops_at_zero == 0
    assert d.n_click_passes_zero == 1

    d.move("L30")
    assert d.pointing_to == 52
    assert d.n_stops_at_zero == 0
    assert d.n_click_passes_zero == 1

    d.move("R48")
    assert d.pointing_to == 0
    assert d.n_stops_at_zero == 1
    assert d.n_click_passes_zero == 2

    d.move("L5")
    assert d.pointing_to == 95
    assert d.n_stops_at_zero == 1
    assert d.n_click_passes_zero == 2

    d.move("R60")
    assert d.pointing_to == 55
    assert d.n_stops_at_zero == 1
    assert d.n_click_passes_zero == 3

    d.move("L55")
    assert d.pointing_to == 0
    assert d.n_stops_at_zero == 2
    assert d.n_click_passes_zero == 4


@pytest.mark.parametrize(
    "move,expected",
    [
        ("R1000", 10),
        ("R49", 0),
        ("R50", 1),
        ("L48", 0),
        ("L49", 0),
        ("L100", 1),
        ("R100", 1),
        ("L200", 2),
        ("R200", 2),
        ("R149", 1),
        ("R150", 2),
        ("R151", 2),
    ],
)
def test_move_multiple_cycles(move, expected):
    d = Dial()
    d.move(move)
    assert d.n_click_passes_zero == expected


@pytest.mark.parametrize(
    "start,move,expected",
    [
        (99, "R1", 1),
        (0, "R100", 1),
        (0, "R99", 0),
    ],
)
def test_move_different_starts(start, move, expected):
    d = Dial()
    d.pointing_to = start
    d.move(move)
    assert d.n_click_passes_zero == expected


def get_passwords(moves):
    d = Dial()
    for move in moves.strip().splitlines():
        d.move(move)
    return d.n_stops_at_zero, d.n_click_passes_zero


def test_get_passwords():
    expected = (3, 6)
    obtained = get_passwords(EXAMPLE)
    assert obtained == expected


def test_dont_ruin_first_answer():
    with open("2025/01/input") as f:
        moves = f.read()
    first_answer, _ = get_passwords(moves)
    assert first_answer == 1168


if __name__ == "__main__":
    with open("2025/01/input") as f:
        moves = f.read()
    print(get_passwords(moves))
