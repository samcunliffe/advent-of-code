import dataclasses


def rank_of(card):
    return "23456789TJQKA".index(card)


@dataclasses.dataclass
class Hand:
    cards: str
    bet: int = 0

    @property
    def _set(self):
        return set(self.cards)

    @property
    def _number_unique_cards(self):
        return len(self._set)

    @property
    def is_five_of_a_kind(self):
        return self._number_unique_cards == 1

    @property
    def is_four_of_a_kind(self):
        if self._number_unique_cards != 2:
            return False
        first, second = self._set
        return self.cards.count(first) == 4 or self.cards.count(second) == 4

    @property
    def is_full_house(self):
        if self._number_unique_cards != 2:
            return False
        first, second = self._set
        return self.cards.count(first) == 3 or self.cards.count(second) == 3

    @property
    def is_three_of_a_kind(self):
        if self._number_unique_cards != 3:
            return False
        return max([self.cards.count(c) for c in self._set]) == 3

    @property
    def is_two_pair(self):
        if self._number_unique_cards != 3:
            return False
        return sorted([self.cards.count(c) for c in self._set]) == [1, 2, 2]

    @property
    def is_one_pair(self):
        if self._number_unique_cards != 4:
            return False
        return max([self.cards.count(c) for c in self._set]) == 2

    @property
    def is_high_card(self):
        return self._number_unique_cards == 5

    @property
    def _type(self):
        """Encode the type of hand as an integer.

        Needed for comparator method. "High card" is 0, the weakest. "Five of a
        kind" is 6, the strongest.
        """
        rules = [
            self.is_high_card,
            self.is_one_pair,
            self.is_two_pair,
            self.is_three_of_a_kind,
            self.is_full_house,
            self.is_four_of_a_kind,
            self.is_five_of_a_kind,
        ]
        return rules.index(True)

    def __gt__(self, other):
        if self._type != other._type:
            return self._type > other._type
        for our_card, other_card in zip(self.cards, other.cards):
            if our_card != other_card:
                return rank_of(our_card) > rank_of(other_card)


def parse_hand_bet(line):
    cards, bet = line.split()
    return Hand(cards, int(bet))


def test_parse_hand_bet():
    assert parse_hand_bet("32T3K 765") == (Hand("32T3K", 765))
    assert parse_hand_bet("T55J5 684") == (Hand("T55J5", 684))


def test_hand_type_logic():
    assert Hand("32T3K").is_five_of_a_kind is False
    assert Hand("32T3K").is_four_of_a_kind is False
    assert Hand("32T3K").is_full_house is False
    assert Hand("32T3K").is_three_of_a_kind is False
    assert Hand("32T3K").is_two_pair is False
    assert Hand("32T3K").is_one_pair is True
    assert Hand("32T3K").is_high_card is False
    assert Hand("32T3K")._type == 1

    assert Hand("QQQJA").is_five_of_a_kind is False
    assert Hand("QQQJA").is_four_of_a_kind is False
    assert Hand("QQQJA").is_full_house is False
    assert Hand("QQQJA").is_three_of_a_kind is True
    assert Hand("QQQJA").is_two_pair is False
    assert Hand("QQQJA").is_one_pair is False
    assert Hand("QQQJA").is_high_card is False
    assert Hand("QQQJA")._type == 3


def test_hand_comparisons():
    assert Hand("QQQJA") > Hand("32T3K")

    assert Hand("KK677").is_two_pair is True
    assert Hand("KTJJT").is_two_pair is True
    assert Hand("KK677") > Hand("KTJJT")


def score_hands(hands):
    hands.sort()
    return sum([hand.bet * (hand_rank + 1) for hand_rank, hand in enumerate(hands)])


def test_full_scoring_example_data():
    test_data = """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
    """
    hands = [parse_hand_bet(line) for line in test_data.strip().split("\n")]
    assert score_hands(hands) == 6440


with open("2023/7/input.txt") as fi:
    hands = [parse_hand_bet(line) for line in fi]
    answer = score_hands(hands)
    print(answer)
