import sys
from pathlib import Path
import logging
import numpy as np

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def valid_condition(up_pattern, down_pattern):
        return (up_pattern == down_pattern).all()

    def process_horizontal_pattern(self, pattern) -> int:
        for i in range(1, len(pattern)):
            N = pattern.shape[0]
            if i <= N / 2:
                up_pattern = pattern[:i]
            else:
                up_pattern = pattern[2*i - N:i]
            down_pattern = pattern[i: i + len(up_pattern)]
            if self.valid_condition(up_pattern, down_pattern[::-1]):
                return i
        return 0

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().split('\n\n')
        result = 0
        for i, pattern in enumerate(input_data):
            pattern = pattern.split()
            pattern = np.array(list(map(list, pattern)))
            h_pattern = self.process_horizontal_pattern(pattern)
            v_pattern = self.process_horizontal_pattern(pattern.T)
            result += 100*h_pattern + v_pattern
        return result


class Part2(Part1):
    @staticmethod
    def valid_condition(up_pattern, down_pattern):
        return (up_pattern != down_pattern).sum() == 1


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 13

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 405
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 400

    print("Test ok")

    # logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # # logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
