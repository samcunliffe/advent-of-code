import pytest
import itertools


EXAMPLE = """
987654321111111
811111111111119
234234234234278
818181911112111"""


def max_joltage(bank, n_batteries=2):
    return int("".join(max(set(itertools.combinations(bank, n_batteries)))))


@pytest.mark.parametrize(
    "bank,expected",
    [
        ("987654321111111", 98),
        ("811111111111119", 89),
        ("234234234234278", 78),
        ("818181911112111", 92),
    ],
)
def test_max_joltage(bank, expected):
    obtained = max_joltage(bank)
    assert obtained == expected


def sum_max_joltage(banks, n_batteries=2):
    return sum(max_joltage(bank, n_batteries) for bank in banks)


def test_example():
    banks = EXAMPLE.strip().split("\n")
    obtained = sum_max_joltage(banks)
    assert obtained == 357


def test_example2():
    banks = EXAMPLE.strip().split("\n")
    obtained = sum_max_joltage(banks, n_batteries=12)
    assert obtained == 3121910778619


if __name__ == "__main__":
    with open("2025/03/input") as f:
        banks = f.read().strip().split("\n")
    print(sum_max_joltage(banks))
    # print(sum_max_joltage(banks, n_batteries=12))
