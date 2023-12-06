def cleaned(numbers):
    return set([n.strip().rstrip() for n in numbers.split(" ") if n != ""])


def parse_card(card):
    _, scratched = card.split(":")
    winning_numbers, our_numbers = scratched.split("|")
    return cleaned(winning_numbers), cleaned(our_numbers)


def number_of_matches(winning_numbers, our_numbers):
    return len(winning_numbers.intersection(our_numbers))


def score(n_matches):
    return 0 if n_matches <= 0 else 2 ** (n_matches - 1)


def score_card(card):
    winning_numbers, our_numbers = parse_card(card)
    return score(number_of_matches(winning_numbers, our_numbers))


def test_score_card():
    assert score_card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53") == 8
    assert score_card("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19") == 2
    assert score_card("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83") == 1
    assert score_card("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36") == 0


with open("2023/4/input.txt") as fi:
    answer = sum([score_card(line) for line in fi])
    print(answer)
