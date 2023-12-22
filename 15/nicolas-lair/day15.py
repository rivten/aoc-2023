import sys
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Part1:
    @staticmethod
    def hash_map(s: str):
        hash = 0
        for c in s:
            hash += ord(c)
            hash *= 17
            hash %= 256
        return hash

    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read()
        result = 0

        for s in input_data.strip().split(","):
            hash = self.hash_map(s)
            logger.debug(hash)
            result += hash
        return result


class Part2(Part1):
    def run(self, input_filename: str):
        logger.info(f"Using data from {input_filename}")
        with open(data_folder / input_filename, "r") as input_txt:
            input_data = input_txt.read().strip()

        lens_boxes = {k: {} for k in range(256)}
        for s in input_data.split(","):
            if s[-1].isdigit():
                box = self.hash_map(s[:-2])
                lens_boxes[box][s[:-2]] = int(s[-1])
            else:
                box = self.hash_map(s[:-1])
                try:
                    lens_boxes[box].pop(s[:-1])
                except KeyError:
                    pass

        result = 0
        for box, lens in lens_boxes.items():
            for pos, focal in enumerate(lens.values()):
                result += (box + 1) * (pos + 1) * focal
        return result


if __name__ == "__main__":
    data_folder = Path(r"C:\Users\nlair\Downloads")
    day = 15

    # Test on examples
    logger.setLevel(logging.DEBUG)
    assert Part1().run(input_filename=f"day{day}_ex.txt") == 1320
    assert Part2().run(input_filename=f"day{day}_ex.txt") == 145
    #
    print("Test ok")

    logger.setLevel(logging.INFO)
    print("Part1 result")
    print(Part1().run(input_filename=f"day{day}.txt"))
    #
    # # logger.setLevel(logging.INFO)
    print("Part2 result")
    print(Part2().run(input_filename=f"day{day}.txt"))
