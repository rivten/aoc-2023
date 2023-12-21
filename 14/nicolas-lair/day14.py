import sys
from pathlib import Path
import logging
import numpy as np

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
      def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read()
        input_data = np.array(list(map(list, input_data.splitlines())))
        nrow, ncols = input_data.shape
        result = 0
        for j in range(ncols):
            col_value = 0
            col = input_data[:, j]
            position = 0
            for chunk in ''.join(col).split('#'):
                if chunk == '':
                    position +=1
                else:
                    n_zero = chunk.count('O')
                    col_value += sum([nrow - position - k for k in range(n_zero)])
                    position += len(chunk) + 1

            # logger.debug((j, col_value))
            result +=col_value
        return result


class Part2:
    def tilt(self, grid, direction):
        slicer, iterator = self.get_tilt_inner_param(grid, direction)
        new_grid = np.empty_like(grid)
        for j in iterator:
            col = grid[slicer(j)]
            new_col = []
            for chunk in ''.join(col.flatten()).split('#'):
                n_rock = chunk.count('O')
                new_col.append('O' * n_rock + '.' * (len(chunk) - n_rock))
            new_col = '#'.join(new_col)
            new_grid[slicer(j)] = np.array(list(new_col)).reshape(new_grid[slicer(j)].shape)
        return new_grid

    def get_tilt_inner_param(self, grid, direction):
        if direction in ['north', 'south']:
            iterator = range(grid.shape[1])
            if direction == 'north':
                slicer = self.get_vertical_slicer(north=True)
            else:
                slicer = self.get_vertical_slicer(north=False)
        else:
            iterator = range(grid.shape[0])
            if direction == 'west':
                slicer = self.get_horizontal_slicer(west=True)
            else:
                slicer = self.get_horizontal_slicer(west=False)
        return slicer, iterator

    @staticmethod
    def get_vertical_slicer(north: bool):
        if north:
            row_slice = slice(None)
        else:
            row_slice = slice(None, None, -1)

        def slicer(param):
            return row_slice, slice(param, param+1)
        return slicer

    @staticmethod
    def get_horizontal_slicer(west: bool):
        if west:
            col_slice = slice(None)
        else:
            col_slice = slice(None, None, -1)

        def slicer(param):
            return slice(param, param + 1), col_slice
        return slicer

    def cycle(self, grid):
        grid = self.tilt(grid, direction='north')
        grid = self.tilt(grid, direction='west')
        grid = self.tilt(grid, direction='south')
        grid = self.tilt(grid, direction='east')
        return grid

    def eval_grid(self, grid):
        return (grid == 'O').sum(axis=1).dot(np.arange(grid.shape[1], 0, -1))

    def run(self, input_filename: str, n_cycles: int):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read()
        grid = np.array(list(map(list, input_data.splitlines())))
        logger.debug(self.print_grid(grid))
        indices_records = []
        in_cycle = False
        begin_indices = []
        cycle_length = -1
        value_cycle = []
        while True:
            next_grid = self.cycle(grid)
            indices = np.argwhere(next_grid != grid).tolist()
            if in_cycle:
                if indices == indices_records[begin_indices[0]]:
                    break
                begin_indices = [ind for ind in begin_indices if indices_records[ind+cycle_length] == indices]
                if begin_indices == []:
                    in_cycle = False
                    cycle_length = -1
                else:
                    cycle_length += 1
                    value_cycle.append(self.eval_grid(next_grid))
            if not in_cycle and indices in indices_records:
                in_cycle = True
                cycle_length = 1
                begin_indices = [i for i, ind in enumerate(indices_records) if ind == indices]
                value_cycle = [self.eval_grid(next_grid)]
            indices_records.append(indices)
            grid = next_grid
        logger.debug((begin_indices[0], cycle_length))
        cycle_pos = (n_cycles - begin_indices[0]) % cycle_length
        return value_cycle[cycle_pos - 1]

if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 14

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 136
    assert Part2().run(input_filename=f"day{day}_ex.txt", n_cycles=int(1e9)) == 64

    print("Test ok")

    # logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # # logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt", n_cycles=int(1e9)))
