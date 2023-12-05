from pathlib import Path
import logging
import sys
import re
import math

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    stock = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    def process_line(self, line: str) -> int:
        game_id, draws = line.split(":")
        for d in draws.split(";"):
            draw_list = [d_.strip().split() for d_ in d.strip().split(',')]
            for nb, color in draw_list:
                if self.stock[color] < int(nb):
                    logger.debug(line)
                    return 0
        game_id = int(game_id.split()[-1])
        return game_id

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        result = 0
        with open(data_folder / input_filename, "r") as input_txt:
            while line := input_txt.readline():
                logger.debug(line)
                result += self.process_line(line)
        return result


class Part2(Part1):
    def process_line(self, line: str) -> int:
        max_cube_in_draw = {'red': 0, 'green': 0, 'blue': 0}
        _, draws = line.split(":")
        for draw in re.split(r";|,", draws):
            nb, color = draw.strip().split()
            max_cube_in_draw[color] = max(max_cube_in_draw[color], int(nb))
        return math.prod(max_cube_in_draw.values())


if __name__ == "__main__":
    data_folder = Path(__file__).parents[1] / "data"
    day=2

    # Test on examples
    logger.setLevel(logging.INFO)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 8
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 2286

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
    
