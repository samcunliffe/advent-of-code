class Sequence:
    def __init__(self, data):
        self.index = 0
        self.data = data

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.index += 1
            return self.data[self.index - 1], self.data[self.index]
        except IndexError:
            self.index = 0
            raise StopIteration

    @property
    def is_non_zero(self):
        return any([element != 0 for element in self.data])

    def first(self):
        return self.data[0]

    def last(self):
        return self.data[-1]


def test_sequence():
    sequence = Sequence([0, 3, 6, 9, 12, 15])
    expected = [(0, 3), (3, 6), (6, 9), (9, 12), (12, 15)]
    for (a, b), (c, d) in zip(sequence, expected):
        assert a == c
        assert b == d


def reduce(sequence):
    return Sequence([b - a for a, b in sequence])


def test_reduce_sequence():
    sequence = Sequence([0, 3, 6, 9, 12, 15])
    for a, b in reduce(sequence):
        assert a == b == 3

    for a, b in reduce(reduce(sequence)):
        assert a == b == 0


def test_non_zero():
    assert Sequence([0, 0, 0, 0, 0, 0]).is_non_zero is False
    assert Sequence([1, 2, 3, 4, 5, 6]).is_non_zero is True


def pairwise_sum(li):
    if len(li) == 1:
        return li[0]
    if len(li) == 2:
        return sum(li)
    return pairwise_sum([li[0] + li[1]] + li[2:])
    # probably can be done better with functools


def test_pairwise_sum():
    assert pairwise_sum([3, 15]) == 18
    assert pairwise_sum([2, 6, 15, 45]) == 68


def find_next(sequence):
    to_sum = []
    while sequence.is_non_zero:
        to_sum.append(sequence.last())
        sequence = reduce(sequence)
    return pairwise_sum(list(reversed(to_sum)))


def test_find_next():
    sequence = Sequence([0, 3, 6, 9, 12, 15])
    assert find_next(sequence) == 18

    sequence = Sequence([1, 3, 6, 10, 15, 21])
    assert find_next(sequence) == 28

    sequence = Sequence([10, 13, 16, 21, 30, 45])
    assert find_next(sequence) == 68


def parse(line):
    return Sequence([int(element) for element in line.split(" ")])


def test_parse_line():
    test_data = "0 3 6 9 12 15"
    expected = [0, 3, 6, 9, 12, 15]
    assert parse(test_data).data == expected


with open("2023/9/input.txt") as fi:
    next_terms = [find_next(parse(line)) for line in fi]
    print(sum(next_terms))


# Part 2


def pairwise_difference(li):
    if len(li) == 1:
        return li[0]
    if len(li) == 2:
        return li[1] - li[0]
    return pairwise_difference([li[1] - li[0]] + li[2:])


def test_pairwise_difference():
    assert pairwise_difference([3, 0]) == -3
    assert pairwise_difference([1, 2, 1]) == 0
    assert pairwise_difference([2, 0, 3, 10]) == 5


def find_previous(sequence):
    to_sum = []
    while sequence.is_non_zero:
        to_sum.append(sequence.first())
        sequence = reduce(sequence)
    return pairwise_difference(list(reversed(to_sum)))


def test_find_previous():
    sequence = Sequence([0, 3, 6, 9, 12, 15])
    assert find_previous(sequence) == -3

    sequence = Sequence([1, 3, 6, 10, 15, 21])
    assert find_previous(sequence) == 0

    sequence = Sequence([10, 13, 16, 21, 30, 45])
    assert find_previous(sequence) == 5


with open("2023/9/input.txt") as fi:
    previous_terms = [find_previous(parse(line)) for line in fi]
    print(sum(previous_terms))
