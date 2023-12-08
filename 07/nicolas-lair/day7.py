import logging
import sys
from pathlib import Path
from enum import StrEnum, Enum
from collections import Counter
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Card(StrEnum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    T = 'T'
    J = 'J'
    Q = 'Q'
    K = 'K'
    A = 'A'

    def __lt__(self, other):
        return Card_value[self] < Card_value[other]


Card_value = {
    Card.TWO: 2,
    Card.THREE: 3,
    Card.FOUR: 4,
    Card.FIVE: 5,
    Card.SIX: 6,
    Card.SEVEN: 7,
    Card.EIGHT: 8,
    Card.NINE: 9,
    Card.TEN: 10,
    Card.T: 11,
    Card.J: 12,
    Card.Q: 13,
    Card.K: 14,
    Card.A: 15,
}


class HandTypeValue(float, Enum):
    SINGLE = 1
    ONEPAIR = 2
    TWOPAIRS = 2.5
    THREE = 3
    FULL = 3.5
    FOUR = 4
    FIVE = 5

Joker_Upgrade = {
    HandTypeValue.SINGLE: HandTypeValue.ONEPAIR,
    HandTypeValue.ONEPAIR: HandTypeValue.THREE,
    HandTypeValue.TWOPAIRS: HandTypeValue.FULL,
    HandTypeValue.THREE: HandTypeValue.FOUR,
    HandTypeValue.FULL: HandTypeValue.FOUR,
    HandTypeValue.FOUR: HandTypeValue.FIVE,
    HandTypeValue.FIVE: HandTypeValue.FIVE,
}


class Hand:
    def __init__(self, input_hand: str, use_j_rule: bool = False):
        card_hand, bid = input_hand.split()
        if card_hand == "KTJJT":
            print(1)
        self.str_card_hand = card_hand
        self.card_list = [Card(c) for c in card_hand]
        self.hand_type: HandTypeValue = self.compute_hand_type(use_j_rule)
        self.bid: int = int(bid)

    @staticmethod
    def _compute_hand_type(card_list) -> HandTypeValue:
        card_counter = sorted(Counter(card_list).values(), reverse=True)
        if card_counter[0] == 5:
            return HandTypeValue.FIVE
        elif card_counter[0] == 4:
            return HandTypeValue.FOUR
        elif card_counter[0] == 3:
            if len(card_counter) > 1 and (card_counter[1] == 2):
                return HandTypeValue.FULL
            else:
                return HandTypeValue.THREE
        elif card_counter[0] == 2:
            if (len(card_counter) > 1) and (card_counter[1] == 2):
                return HandTypeValue.TWOPAIRS
            else:
                return HandTypeValue.ONEPAIR
        else:
            return HandTypeValue.SINGLE

    def __lt__(self, other) -> bool:
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        else:
            for c1, c2 in zip(self.card_list, other.card_list):
                if c1 != c2:
                    return c1 < c2

    def compute_hand_type(self, use_joker_rule: bool = False):
        if use_joker_rule:
            return self._compute_hand_type_with_j_rule()
        else:
            return self._compute_hand_type(self.card_list)

    def _compute_hand_type_with_j_rule(self) -> HandTypeValue:
        card_list_no_J = [c for c in self.card_list if c != Card.J]
        if len(card_list_no_J) == 0:
            normal_hand_type = HandTypeValue(5)
        else:
            normal_hand_type = self._compute_hand_type(card_list_no_J)
        card_counter = Counter(self.card_list)
        n_j_card = card_counter.get(Card.J, 0)
        for _ in range(n_j_card):
            normal_hand_type = Joker_Upgrade[normal_hand_type]
        return normal_hand_type


class Part1:
    @staticmethod
    def run(input_filename: str, use_joker_rule: bool = False):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        hand_list = [Hand(input_hand=h, use_j_rule=use_joker_rule) for h in input_data]
        sorted_hand_list = sorted(hand_list)
        logger.debug([c.str_card_hand for c in sorted_hand_list])
        result = sum([(i+1)*hand.bid for i, hand in enumerate(sorted_hand_list)])
        logger.debug(result)
        return result


class Part2(Part1):
    def run(self, input_filename: str, **kwargs):
        Card_value[Card.J] = -1
        return super().run(input_filename, use_joker_rule=True)


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 7

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 6440
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 5905

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
