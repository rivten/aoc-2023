import logging
import sys
from pathlib import Path
import math

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def compute_delta(d, t):
        return math.sqrt(t**2 - 4*d)

    @staticmethod
    def parse_time_and_distance(input_data: list[str]) -> (list[int], list[int]):
        time = map(int, input_data[0].split()[1:])
        distance = map(int, input_data[1].split()[1:])
        return time, distance

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()
        time, distance = self.parse_time_and_distance(input_data)
        result = 1
        for t, d in zip(time, distance):
            delta = self.compute_delta(d, t)
            n_match = math.ceil((-t + delta) / 2 - 1) - math.floor((-t - delta) / 2 + 1) + 1
            logger.debug((n_match, (-t + delta) / 2, (-t - delta) / 2))
            result *= n_match
        return result


class Part2(Part1):
    @staticmethod
    def parse_time_and_distance(input_data: list[str]) -> (list[int], list[int]):
        time = int(''.join(input_data[0].split()[1:]))
        distance = int(''.join(input_data[1].split()[1:]))
        return [time], [distance]


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 6

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 288
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 71503

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
