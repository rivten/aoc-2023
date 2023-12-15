import logging
import sys
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def run(input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        input_array = np.char.array(list(map(list, input_data)))
        galaxy_shape = input_array.shape
        galaxy_line, galaxy_cols = zip(*np.argwhere(input_array == '#'))
        line_wo_galaxy = set(range(input_array.shape[0])).difference(galaxy_line)
        cols_wo_galaxy = set(range(input_array.shape[1])).difference(galaxy_cols)
        expanded_input_data = input_array.tolist()
        for i in sorted(line_wo_galaxy, reverse=True):
            expanded_input_data.insert(i, ['.']*galaxy_shape[0])
        expanded_input_data = np.array(expanded_input_data).T.tolist()
        for i in sorted(cols_wo_galaxy, reverse=True):
            expanded_input_data.insert(i, ['.']*len(expanded_input_data[0]))
        expanded_input_data = np.char.array(expanded_input_data).T
        galaxies = np.argwhere(expanded_input_data == '#')
        result = 0
        for i in range(len(galaxies)):
            for j in range(i + 1, len(galaxies)):
                result += np.abs(galaxies[i] - galaxies[j]).sum()
        return result

class Part2:
    def is_between(self, x1, x2, y):
        return (y - x1) * (y - x2) < 0

    def run(self, input_filename: str, expansion_size: int):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        input_array = np.char.array(list(map(list, input_data)))
        galaxies= np.argwhere(input_array == '#')
        galaxy_line, galaxy_cols = zip(*galaxies)
        line_wo_galaxy = set(range(input_array.shape[0])).difference(galaxy_line)
        cols_wo_galaxy = set(range(input_array.shape[1])).difference(galaxy_cols)
        result = 0
        for i, g1 in enumerate(galaxies):
            for j in range(i+1, len(galaxies)):
                g2 = galaxies[j]
                n_empty_lines_between = sum([int(self.is_between(g1[0], g2[0], l)) for l in line_wo_galaxy])
                n_empty_cols_between = sum([int(self.is_between(g1[1], g2[1], l)) for l in cols_wo_galaxy])
                n_expansion = n_empty_lines_between + n_empty_cols_between
                result += np.abs(galaxies[i] - galaxies[j]).sum() + n_expansion * (expansion_size -1)
        return result






if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 11

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 374
    assert Part2().run(input_filename=f"day{day}_ex.txt", expansion_size=10) == 1030
    assert Part2().run(input_filename=f"day{day}_ex.txt", expansion_size=100) == 8410

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # # logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt", expansion_size=int(1e6)))
