import sys
from pathlib import Path
import logging
import numpy as np
from enum import IntEnum
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class BeamDir(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

    def is_horizontal(self):
        return bool(self.value % 2)


class Part1:
    @staticmethod
    def get_next_pos(pos, direction, grid_shape):
        if direction == BeamDir.Up:
            x, y = pos[0] - 1, pos[1]
        elif direction == BeamDir.Down:
            x, y = pos[0] + 1, pos[1]
        elif direction == BeamDir.Right:
            x, y = pos[0], pos[1] + 1
        else:
            assert direction == BeamDir.Left
            x, y = pos[0], pos[1] - 1
        return max(0, min(x, grid_shape[0])), max(0, min(y, grid_shape[1]))

    def propagate_beam(self, grid, energized_grid, pos, direction):
        next_pos = self.get_next_pos(pos, direction, grid.shape)
        try:
            if energized_grid[next_pos[0]][next_pos[1]][direction] == 1:
                return
            energized_grid[next_pos[0]][next_pos[1]][direction] = 1
            if grid[next_pos[0]][next_pos[1]] == '\\':
                if direction == BeamDir.Up:
                    next_dir = BeamDir.Left
                elif direction == BeamDir.Down:
                    next_dir = BeamDir.Right
                elif direction == BeamDir.Left:
                    next_dir = BeamDir.Up
                elif direction == BeamDir.Right:
                    next_dir = BeamDir.Down
            elif grid[next_pos[0]][next_pos[1]] == '/':
                if direction == BeamDir.Up:
                    next_dir = BeamDir.Right
                elif direction == BeamDir.Down:
                    next_dir = BeamDir.Left
                elif direction == BeamDir.Left:
                    next_dir = BeamDir.Down
                elif direction == BeamDir.Right:
                    next_dir = BeamDir.Up
            elif ((grid[next_pos[0]][next_pos[1]] == '.')
                  or (not direction.is_horizontal() and grid[next_pos[0]][next_pos[1]] == '|')
                  or (direction.is_horizontal() and grid[next_pos[0]][next_pos[1]] == '-')):
                next_dir = direction
            else:
                if grid[next_pos[0]][next_pos[1]] == '|':
                    assert direction.is_horizontal()
                    self.propagate_beam(grid, energized_grid, next_pos, BeamDir.Up)
                    self.propagate_beam(grid, energized_grid, next_pos, BeamDir.Down)
                elif grid[next_pos[0]][next_pos[1]] == '-':
                    assert not direction.is_horizontal()
                    self.propagate_beam(grid, energized_grid, next_pos, BeamDir.Left)
                    self.propagate_beam(grid, energized_grid, next_pos, BeamDir.Right)
                else:
                    raise NotImplementedError
                return
            self.propagate_beam(grid, energized_grid, next_pos, next_dir)
        except IndexError:
            return

    @staticmethod
    def eval_grid(energized_grid):
        return (energized_grid.sum(axis=2) != 0).sum()

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        grid = np.array(list(map(list, input_data)))
        energized_grid = np.zeros((*grid.shape, 4))
        self.propagate_beam(grid, energized_grid, (0, -1), BeamDir.Right)
        logger.debug(energized_grid)
        return self.eval_grid(energized_grid)


class Part2(Part1):
    def run(self, input_filename: str):

        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().splitlines()

        grid = np.array(list(map(list, input_data)))
        result = 0
        for i in range(grid.shape[0]):
            energized_grid = np.zeros((*grid.shape, 4))
            self.propagate_beam(grid, energized_grid, (i, -1), BeamDir.Right)
            result = max(result, self.eval_grid(energized_grid))
            energized_grid = np.zeros((*grid.shape, 4))
            self.propagate_beam(grid, energized_grid, (i, grid.shape[1]), BeamDir.Left)
            result = max(result, self.eval_grid(energized_grid))

        for j in range(grid.shape[1]):
            energized_grid = np.zeros((*grid.shape, 4))
            self.propagate_beam(grid, energized_grid, (-1, j), BeamDir.Down)
            result = max(result, self.eval_grid(energized_grid))
            energized_grid = np.zeros((*grid.shape, 4))
            self.propagate_beam(grid, energized_grid, (grid.shape[0], j), BeamDir.Up)
            result = max(result, self.eval_grid(energized_grid))

        return result


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 16

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 46
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 51
    #
    print("Test ok")

    logger.setLevel(logging.INFO)
    import sys
    sys.setrecursionlimit(10000)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # # logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
