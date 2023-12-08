import logging
import sys
from pathlib import Path
from math import lcm
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def parse_data(input_filename):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        instructions = input_data.pop(0)
        node_map = {}
        for line in input_data[1:]:
            node, left, right = line[:3], line[7:10], line[12:15]
            node_map[node] = (left, right)
        return instructions, node_map

    def run(self, input_filename: str):
        instructions, node_map = self.parse_data(input_filename)
        position = 'AAA'
        n_steps = 0
        while position != 'ZZZ':
            n_steps += len(instructions)
            for i in instructions:
                dir = 1 if i == 'R' else 0
                position = node_map[position][dir]
        logger.debug(n_steps)
        return n_steps


class Part2(Part1):
    def run(self, input_filename: str) -> int:
        instructions, node_map = self.parse_data(input_filename)

        starting_node = set(node for node in node_map.keys() if node[-1] == 'A')

        position_by_starting_pos = {
            s: s for s in starting_node
        }
        position_end_list = {
            s: [] for s in starting_node
        }
        while len(position_by_starting_pos) > 0:
            for i in instructions:
                dir = 1 if i == 'R' else 0
                for s, pos in position_by_starting_pos.items():
                    position_by_starting_pos[s] = node_map[pos][dir]

            for s in list(position_by_starting_pos):
                pos = position_by_starting_pos[s]
                if pos not in position_end_list[s]:
                    position_end_list[s].append(pos)
                else:
                    position_by_starting_pos.pop(s)

        path_length_by_starting_pos = {s: len(pos) for s, pos in position_end_list.items()}
        lcm_value = lcm(*path_length_by_starting_pos.values())
        return lcm_value * len(instructions)


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 8

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex1.txt") == 2
    assert Part1().run(input_filename=f"day{day}_ex2.txt") == 6
    assert Part2().run(input_filename=f"day{day}_ex3.txt") == 6

    print("Test ok")

    # logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # # logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
    print(1)
