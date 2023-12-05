import itertools

red = "red"
green = "green"
blue = "blue"


def get_grid():
    grid = []
    with open("input_03.txt", "r") as f:
        for ln in f:
            row = []
            for c in ln:
                row.append(c)
            grid.append(row)
    return grid


def puzzle1():
    grid = get_grid()
    numbers_by_pos_and_length = get_numbers_by_position_and_length(grid)
    symbols = get_symbols(grid)
    (X, Y) = len(grid[0]), len(grid)

    res = 0

    for ((x, y, n), number) in numbers_by_pos_and_length.items():
        range_x = [x + t - 1 for t in range(n + 2) if x + t not in [-1, X]]
        range_y = [t for t in [y - 1, y, y + 1] if t not in [-1, Y]]
        pos_to_check = set(itertools.product(range_x, range_y))
        # I know, we are including the positions of the number itself which we already know are not symbols,
        # but what the hell
        if len(pos_to_check.intersection(symbols)) > 0:
            res += number
    print(res)


def puzzle2():
    grid = get_grid()
    numbers_by_pos_and_length = get_numbers_by_position_and_length(grid)
    symbols = get_symbols(grid, filtered_char='*')
    (X, Y) = len(grid[0]), len(grid)

    symbols_adjacencies = {t:[] for t in symbols}
    for ((x, y, n), number) in numbers_by_pos_and_length.items():
        range_x = [x + t - 1 for t in range(n + 2) if x + t not in [-1, X]]
        range_y = [t for t in [y - 1, y, y + 1] if t not in [-1, Y]]
        pos_to_check = set(itertools.product(range_x, range_y))
        # I know, we are including the positions of the number itself which we already know are not symbols,
        # but what the hell
        for t in pos_to_check.intersection(symbols):
            symbols_adjacencies[t].append(number)

    print(sum(t[0]*t[1] for t in symbols_adjacencies.values() if len(t)==2))



def process_number(number):
    res = 0
    for c in number:
        res = 10 * res + int(c)
    return res


def get_numbers_by_position_and_length(grid):
    numbers_by_pos_and_length = {}

    for (y, row) in enumerate(grid):
        number = []
        pos_number_start = 0
        for (x, c) in enumerate(row):
            if c.isdigit():
                if len(number) == 0:
                    pos_number_start = x
                number.append(c)
            elif len(number) > 0:
                numbers_by_pos_and_length[pos_number_start, y, len(number)] = process_number(number)
                number = []
    return numbers_by_pos_and_length


def get_symbols(grid, filtered_char=None):
    symbols = []
    for (y, row) in enumerate(grid):
        for (x, c) in enumerate(row):
            if filtered_char is None and not c.isdigit() and not c.isalpha() and c != '.':
                symbols.append((x, y))
            if filtered_char is not None and c == filtered_char:
                symbols.append((x, y))
    return symbols


puzzle1()
puzzle2()
