import logging
import sys
from pathlib import Path
from collections import namedtuple
from typing import Union

import numpy as np

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Position(tuple):
    def __new__(cls, x: int, y: int):
        return tuple.__new__(cls, (x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def west(self):
        return Position(self.x, self.y-1)

    def east(self):
        return Position(self.x, self.y + 1)

    def north(self):
        return Position(self.x-1, self.y)

    def south(self):
        return Position(self.x+1, self.y)


class Tile:
    def __init__(self, tile_pos: Position, tile_str: str):
        self.position = tile_pos
        self.tile_str =tile_str
        self.connecting_tile = ()
        if tile_str == '|':
            self.connecting_tile = tile_pos.north(), tile_pos.south()
        elif tile_str == '-':
            self.connecting_tile = tile_pos.east(), tile_pos.west()
        elif tile_str == 'L':
            self.connecting_tile = tile_pos.north(), tile_pos.east()
        elif tile_str == 'J':
            self.connecting_tile = tile_pos.west(), tile_pos.north()
        elif tile_str == '7':
            self.connecting_tile = tile_pos.west(), tile_pos.south()
        elif tile_str == 'F':
            self.connecting_tile = tile_pos.south(), tile_pos.east()

    def next_position(self, current_position):
        if isinstance(current_position, Tile):
            current_position = current_position.position
        if current_position == self.connecting_tile[0]:
            return self.connecting_tile[1]
        if current_position == self.connecting_tile[1]:
            return self.connecting_tile[0]
        raise ValueError

    def connects_to(self, current_position) -> bool:
        if isinstance(current_position, Tile):
            current_position = current_position.position
        return current_position in self.connecting_tile


unconnected_tile = Tile(Position(-1, -1), '')


class Part1:
    @staticmethod
    def build_tile_map(input_data) -> (dict[Tile], Position):
        tile_map = {}
        for i, line in enumerate(input_data):
            for j, tile_str in enumerate(line):
                if tile_str == 'S':
                    starting_position = Position(i, j)
                if tile_str != '.':
                    tile_map[Position(i, j)] = Tile(Position(i, j), tile_str)
        return tile_map, starting_position

    @staticmethod
    def get_admissible_tile_from_start(starting_position, tile_map):
        admissible_position = [
            starting_position.east(), starting_position.west(), starting_position.north(), starting_position.south()
        ]
        admissible_tiles = [tile_map[t] for t in admissible_position if tile_map.get(t, unconnected_tile).connects_to(Tile(starting_position, ''))]
        return admissible_tiles

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        tile_map, starting_position = self.build_tile_map(input_data)
        admissible_tiles = self.get_admissible_tile_from_start(starting_position, tile_map)

        previous_tile = [tile_map[starting_position]]*len(admissible_tiles)
        current_tile = [tile for tile in admissible_tiles]
        path_length = 1
        while True:
            next_tile = [tile_map[cur_tile.next_position(prev_tile)] for cur_tile, prev_tile in zip(current_tile, previous_tile)]
            path_length += 1
            if len(next_tile) != len(set(next_tile)) or set(next_tile).intersection(set(current_tile)):
                break
            previous_tile, current_tile = zip(
                *[(curr_tile, nx_tile) for curr_tile, nx_tile in zip(current_tile, next_tile)
                  if tile_map.get(nx_tile.position, unconnected_tile).connects_to(curr_tile)
                  ]
            )
        return path_length


class Part2(Part1):
    @staticmethod
    def get_starting_position_shape(starting_position, last_position, second_position):
        second_position, last_position = sorted([last_position, second_position])
        if last_position.y == second_position.y:
            return '-'
        elif last_position.x == second_position.x:
            return '|'
        elif last_position.north() == starting_position:
            return 'F'
        elif last_position.south() == starting_position:
            return 'L'
        elif second_position.north() == starting_position:
            return '7'
        elif second_position.south() == starting_position:
            return 'J'
        else:
            raise ValueError

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        tile_map, starting_position = self.build_tile_map(input_data)
        admissible_tiles = self.get_admissible_tile_from_start(starting_position, tile_map)

        for ad_tile in admissible_tiles:
            path = [starting_position, ad_tile.position]
            path_found = False
            while True:
                next_position = tile_map[path[-1]].next_position(path[-2])
                if next_position == path[0]:
                    path_found = True
                    break
                if tile_map[next_position].connects_to(path[-1]):
                    path.append(next_position)
                else:
                    break
            if path_found:
                break

        tile_map[starting_position] = Tile(starting_position,
                                           tile_str=self.get_starting_position_shape(starting_position, path[-1], path[1]))

        map_array = np.zeros((len(input_data), len(input_data[0])))
        map_array_no_horizontal = np.zeros_like(map_array).astype(int)
        for p in path:
            map_array[p] = 1
            if tile_map[p].tile_str == '|':
                map_array_no_horizontal[p] = 1

        turning_pipe_list = [p for p in path if tile_map[p].tile_str in ['F', '7', 'J', 'L']]
        n_pipe = len(turning_pipe_list)
        turning_pipe_list = turning_pipe_list + [turning_pipe_list[0]]
        for i in range(n_pipe):
            p1, p2 = turning_pipe_list[i], turning_pipe_list[i+1]
            if p1.x == p2.x:
                x_p1 = [p.x for p in tile_map[p1].connecting_tile if p.x != p1.x][0]
                x_p2 = [p.x for p in tile_map[p2].connecting_tile if p.x != p2.x][0]
                if x_p1 != x_p2:
                    map_array_no_horizontal[p1] = 1

        print('\n'.join(input_data))
        print(map_array_no_horizontal)
        n_crossing = map_array_no_horizontal.cumsum(axis=1)
        is_interior = (n_crossing % 2)
        valid_interior_tile = is_interior.astype(bool) & ~map_array.astype(bool)
        print(valid_interior_tile.astype(int))
        return valid_interior_tile.sum()


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 10

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex1.txt") == 4
    assert Part1().run(input_filename=f"day{day}_ex2.txt") == 8
    assert Part2().run(input_filename=f"day{day}_ex3.txt") == 4
    assert Part2().run(input_filename=f"day{day}_ex4.txt") == 4
    assert Part2().run(input_filename=f"day{day}_ex5.txt") == 8
    assert Part2().run(input_filename=f"day{day}_ex6.txt") == 10

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # # logger.setLevel(logging.INFO)
    print("Part2 result")
    # Does not work on my input data output 340 vs 337 true response
    print(Part2().run(input_filename=f"day{day}.txt"))
