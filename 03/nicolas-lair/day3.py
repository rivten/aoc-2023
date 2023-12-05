from pathlib import Path
import logging
import sys
import numpy as np
from itertools import product

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def run(input_filename: str):
        logger.info(f"Using data from {input_filename}")
        result = []
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()
        input_data = np.char.array([list(line) for line in input_data])
        symbol_mask = ~(input_data.isdigit() | input_data.endswith('.'))
        n_line, n_char = input_data.shape
        for i, line in enumerate(input_data.tolist()):
            logger.debug((i, line))
            curr_number = ''
            keep = False
            for j, char in enumerate(line):
                logger.debug(char)
                if char.isdigit():
                    curr_number += char
                    if not keep:
                        keep = symbol_mask[max(0, i-1):min(n_line, i + 2),max(0, j-1):min(j+2,n_char)].any().item()
                else:
                    if keep & (curr_number != ''):
                        result.append(int(curr_number))
                    curr_number = ''
                    keep = False
            if keep & (curr_number != ''):
                result.append(int(curr_number))
        logger.info(result)
        return sum(result)


class Part2(Part1):
    @staticmethod
    def run(input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()
        input_data = np.char.array([list(line) for line in input_data])
        star_mask = input_data.endswith('*')
        stars_index = set(map(tuple, np.argwhere(star_mask).tolist()))
        gear = {s_index: [] for s_index in stars_index}
        n_line, n_char = star_mask.shape
        for i, line in enumerate(input_data.tolist()):
            logger.debug((i, line))
            curr_number = ''
            s_index = None
            for j, char in enumerate(line):
                logger.debug(char)
                if char.isdigit():
                    curr_number += char
                    if s_index is None:
                        adjacent_pos = set(
                            product(
                                range(max(0, i - 1), min(n_line, i + 2)),
                                range(max(0, j - 1), min(j + 2, n_char))
                            )
                        )
                        admissible_pos = adjacent_pos.intersection(stars_index)
                        if len(admissible_pos) == 1:
                            s_index = admissible_pos.pop()
                else:
                    if (s_index is not None) & (curr_number != ''):
                        gear[s_index].append(int(curr_number))
                    curr_number = ''
                    s_index= None
            if (s_index is not None) & (curr_number != ''):
                gear[s_index].append(int(curr_number))
        logger.info(gear)
        result = 0
        for g in gear.values():
            if len(g) == 2:
                result += g[0] * g[1]
        return result


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day=3

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 4361
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 467835

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
