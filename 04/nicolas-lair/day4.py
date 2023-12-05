from pathlib import Path
import logging
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def _compute_matching_numbers(line):
        card, numbers = line.split(':')
        winning_numbers, hold_numbers = numbers.strip().split('|')
        winning_numbers = set(map(int, winning_numbers.strip().split()))
        hold_numbers = set(map(int, hold_numbers.strip().split()))
        nb_matching_numbers = len(hold_numbers.intersection(winning_numbers))
        return nb_matching_numbers

    def process_line(self, line: str) -> int:
        nb_matching_numbers = self._compute_matching_numbers(line)
        logger.debug(nb_matching_numbers)
        if nb_matching_numbers > 0:
            return 2**(nb_matching_numbers-1)
        else:
            return 0

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        result = 0
        with open(data_folder / input_filename, "r") as input_txt:
            while line := input_txt.readline():
                logger.debug(line)
                result += self.process_line(line)
        return result


class Part2(Part1):
    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()
        nb_card_occurrences = [1]*len(input_data)
        for i, line in enumerate(input_data):
            nb_matching_numbers = self._compute_matching_numbers(line)
            for j in range(nb_matching_numbers):
                nb_card_occurrences[i+j+1] += nb_card_occurrences[i]
        logger.debug(nb_card_occurrences)
        return sum(nb_card_occurrences)


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day=4

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 13
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 30

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
