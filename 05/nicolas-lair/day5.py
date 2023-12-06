import logging
import sys
from pathlib import Path
from collections import namedtuple

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


Interval = namedtuple('Interval', ['start', 'range'], defaults=(None, None), rename=True)


class PuzzleMap:
    def __init__(self, map_puzzle_input: str):
        map_puzzle_input = map_puzzle_input.splitlines()
        self.name = map_puzzle_input.pop(0)
        map_puzzle_input = map(lambda x: x.strip().split(), map_puzzle_input)
        self.map_puzzle_input = [list(map(int, l_)) for l_ in map_puzzle_input]
        self.map_puzzle_input = sorted(self.map_puzzle_input, key=lambda x: x[1])

    def __getitem__(self, item: int):
        for i, (y_min, x_min, range_val) in enumerate(self.map_puzzle_input):
            if x_min <= item < x_min + range_val:
                return y_min + item - x_min
            elif item < x_min:
                break
        return item

    def map_one_interval(self, source_interval: Interval) -> list[Interval]:
        destination_interval = Interval()
        for (y_min, x_min, range_val) in self.map_puzzle_input:
            if source_interval.start < x_min:
                destination_interval = Interval(
                    start = source_interval.start,
                    range = min(source_interval.range, x_min - source_interval.start)
                )
                break
            elif x_min <= source_interval.start < x_min + range_val:
                destination_interval = Interval(
                    start = y_min + source_interval.start - x_min,
                    range = min(source_interval.range, x_min + range_val - source_interval.start)
                )
                break
        # If source_start is above all map value
        if destination_interval.start is None:
            destination_interval = source_interval

        destination_int_list = [destination_interval]
        if destination_interval.range != source_interval.range:
            remaining_interval = Interval(
                start=source_interval.start + destination_interval.range,
                range=source_interval.range - destination_interval.range)
            destination_int_list += self.map_one_interval(remaining_interval)
        return destination_int_list

    def map_intervals(self, source_intervals: list[Interval]) -> list[Interval]:
        destination_intervals = []
        for s_int in source_intervals:
            destination_intervals += self.map_one_interval(s_int)
            logger.debug((s_int, destination_intervals))
        return destination_intervals


class Part1:
    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read()

        input_data = input_data.split("\n\n")
        seed = map(int, input_data.pop(0).split()[1:])
        chained_map = [
            PuzzleMap(input_map_data) for input_map_data in input_data
        ]
        min_location_number = 9e18
        for s in seed:
            logger.debug(f"Seed: {s}")
            obj = s
            for pmap in chained_map:
                obj = pmap[obj]
                logger.debug(obj)
            min_location_number = min(min_location_number, obj)
        return min_location_number


class Part2(Part1):
    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read()

        input_data = input_data.split("\n\n")
        seed = list(map(int, input_data.pop(0).split()[1:]))
        source_intervals = [Interval(start=seed[2*i], range=seed[2*i+1]) for i in range(len(seed) // 2)]
        logger.debug(source_intervals)
        chained_map = [
            PuzzleMap(input_map_data) for input_map_data in input_data
        ]
        for pmap in chained_map:
            logger.debug(pmap.name)
            source_intervals = pmap.map_intervals(source_intervals)
        min_location_number = min(source_intervals, key=lambda x: x.start).start
        return min_location_number


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 5

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 35
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 46

    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
