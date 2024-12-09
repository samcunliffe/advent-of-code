import re


def find_muls(memory: str) -> list:
    return re.findall(r"mul\((\d+),(\d+)\)", memory)


EXAMPLE_MEMORY = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"


def test_finding():
    assert find_muls(EXAMPLE_MEMORY) == [("2", "4"), ("5", "5"), ("11", "8"), ("8", "5")]


def do_muls(valid_pairs: list[tuple[str, str]]) -> int:
    return [int(x) * int(y) for x, y in valid_pairs]


def test_doing():
    assert do_muls([("2", "4"), ("5", "5"), ("11", "8"), ("8", "5")]) == [8, 25, 88, 40]


def test_finding_and_doing():
    assert sum(do_muls(find_muls(EXAMPLE_MEMORY))) == 161


def read() -> str:
    with open("2024/03/input") as f:
        return f.read()


def main():
    memory = read()
    print("Part 1", sum(do_muls(find_muls(memory))))


if __name__ == "__main__":
    main()
