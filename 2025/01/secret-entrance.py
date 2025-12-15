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


class Cycle:
    def __init__(self):
        self.index = 50
        self.actual_password = 0

    def move(self, move):
        direction, steps = move[0], move[1:]

        if direction not in ("L", "R") or not steps.isdigit():
            raise ValueError("Invalid move")

        direction = -1 if direction == "L" else 1
        steps = int(steps)

        self.index = (self.index + direction * steps) % 100

        if self.index == 0:
            self.actual_password += 1


def test_move():
    cycle = Cycle()
    cycle.move("L68")
    assert cycle.index == 82
    assert cycle.actual_password == 0

    cycle.move("L30")
    assert cycle.index == 52

    cycle.move("R48")
    assert cycle.index == 0
    assert cycle.actual_password == 1


def get_password(moves):
    cycle = Cycle()
    for move in moves.strip().splitlines():
        cycle.move(move)
    return cycle.actual_password


def test_get_password():
    assert get_password(EXAMPLE) == 3


if __name__ == "__main__":
    with open("2025/01/input") as f:
        moves = f.read()
    print(get_password(moves))
