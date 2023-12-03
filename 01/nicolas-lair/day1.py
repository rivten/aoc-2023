from pathlib import Path
import logging
import sys
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def process_line(line: str) -> int:
        first_digit = None
        last_digit = None
        for char in line:
            logger.debug(char)
            if char.isdigit():
                if first_digit is None:
                    first_digit = char
                    last_digit = char
                else:
                    last_digit = char
        logger.debug((first_digit, last_digit))
        return int(first_digit + last_digit)

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        result = 0
        with open(data_folder / input_filename, "r") as input_txt:
            while line := input_txt.readline():
                logger.debug(line)
                result += self.process_line(line)
        return result


str_digits_to_int = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


class Part2(Part1):
    forward_regex = re.compile(r"|".join(list(str_digits_to_int.keys()) + [r"\d"]))
    reverse_regex = re.compile(r"|".join([d[::-1] for d in str_digits_to_int.keys()] + [r"\d"]))

    def get_first_digit(self, line) -> int:
        digit = self.forward_regex.search(line)[0]
        return self.digit_to_int(digit)

    def get_last_digit(self, line) -> int:
        digit = self.reverse_regex.search(line[-2::-1])[0][::-1]
        return self.digit_to_int(digit)

    @staticmethod
    def digit_to_int(digit: str) -> int:
        if digit.isdigit():
            return int(digit)
        else:
            return str_digits_to_int[digit]

    def process_line(self, line):
        first_digit = self.get_first_digit(line)
        last_digit = self.get_last_digit(line)
        logger.debug((first_digit, last_digit))
        return first_digit*10+last_digit


if __name__ == "__main__":
    data_folder = Path(__file__).parents[1] / "data"

    # Test on examples
    assert Part1().run(input_filename="day1_ex.txt") == 142
    logger.setLevel(logging.DEBUG)
    assert Part2().run(input_filename="day1_ex_part2.txt") == 281

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename="day1.txt"))

    print("Part2 result")
    print(Part2().run(input_filename="day1.txt"))
