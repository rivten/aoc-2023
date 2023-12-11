import itertools
import math


def puzzle(expansion_factor):
    galaxies = get_galaxies()
    non_expended_rows = set([x for (x, y) in galaxies])
    expended_rows = [x for x in range(max(non_expended_rows)) if x not in non_expended_rows]
    non_expended_cols = set([y for (x, y) in galaxies])
    expended_cols = [y for y in range(max(non_expended_cols)) if y not in non_expended_cols]
    res = 0
    for ((x1, y1), (x2, y2)) in itertools.product(galaxies, galaxies):
        res += math.fabs(y2 - y1) + math.fabs(x2 - x1)
        res += (expansion_factor - 1) * len([x for x in expended_rows if x1 < x < x2 or x2 < x < x1])
        res += (expansion_factor - 1) * len([y for y in expended_cols if y1 < y < y2 or y2 < y < y1])
    res = res // 2
    print(res)


def puzzle1():
    puzzle(expansion_factor=2)


def puzzle2():
    puzzle(expansion_factor=1000000)


def get_galaxies():
    galaxies = []
    with open("input_11.txt", "r") as f:
        for (y, ln) in enumerate(f):
            for (x, t) in enumerate(ln):
                if t == '#':
                    galaxies.append((x, y))
    return galaxies


puzzle1()
puzzle2()
