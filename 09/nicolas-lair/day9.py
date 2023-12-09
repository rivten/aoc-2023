import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def get_next_line(int_list: list[int]) -> list[int]:
        result = []
        for i in range(len(int_list) - 1):
            result.append(int_list[i+1] - int_list[i])
        return result

    def predict(self, line: str) -> int:
        logger.debug(line)
        int_list = list(map(int, line.split()))
        result_forward = int_list[-1]
        while sum(int_list) != 0:
            int_list = self.get_next_line(int_list)
            result_forward += int_list[-1]
        logger.debug(f'Forward result: {result_forward}')
        return result_forward

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        result = 0
        for line in input_data:
            result += self.predict(line)
        return result


class Part2(Part1):
    def predict(self, line: str) -> int:
        logger.debug(line)
        int_list = list(map(int, line.split()))
        result_backward = int_list[0]
        n_step = 0
        while sum(int_list) != 0:
            int_list = self.get_next_line(int_list)
            n_step += 1
            sign_factor = (n_step % 2 == 0) - (n_step % 2 == 1)
            result_backward += sign_factor * int_list[0]
        logger.debug(f'Backward result: {result_backward}')
        return result_backward


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 9

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 114
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 2
    # assert Part2().run(input_filename=f"day{day}_ex3.txt") == 6

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # # logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
