ROUND = "O"
CUBE = "#"
VOID = "."


def tilt_north(stones, ny, nx):
    for i in range(nx):
        stop_pos = 0
        for j in range(ny):
            if stones[j][i] == ROUND:
                stones[j][i] = VOID
                stones[stop_pos][i] = ROUND
                stop_pos += 1
            elif stones[j][i] == CUBE:
                stop_pos = j + 1


def tilt_south(stones, ny, nx):
    for i in range(nx):
        stop_pos = ny - 1
        for j in range(ny):
            rj = ny - j - 1
            if stones[rj][i] == ROUND:
                stones[rj][i] = VOID
                stones[stop_pos][i] = ROUND
                stop_pos -= 1
            elif stones[rj][i] == CUBE:
                stop_pos = rj - 1


def tilt_east(stones, ny, nx):
    for j in range(ny):
        stop_pos = nx - 1
        for i in range(nx):
            ri = nx - i - 1
            if stones[j][ri] == ROUND:
                stones[j][ri] = VOID
                stones[j][stop_pos] = ROUND
                stop_pos -= 1
            elif stones[j][ri] == CUBE:
                stop_pos = ri - 1


def tilt_west(stones, ny, nx):
    for j in range(ny):
        stop_pos = 0
        for i in range(nx):
            if stones[j][i] == ROUND:
                stones[j][i] = VOID
                stones[j][stop_pos] = ROUND
                stop_pos += 1
            elif stones[j][i] == CUBE:
                stop_pos = i + 1


def spin_cycle(stone, nx, ny):
    tilt_north(stone, nx, ny)
    tilt_west(stone, nx, ny)
    tilt_south(stone, nx, ny)
    tilt_east(stone, nx, ny)


# def get_score(stone, nx, ny):
#     res = 0
#     stone
#     for j,row in enumerate(stone):
#         for i,val in enumerate(row):
#             if val == ROUND:


def display(stones):
    for row in stones:
        print("".join(row))
    print("")


def puzzle1():
    stones = get_stones()
    ny = len(stones)
    nx = len(stones[0])
    tilt_north(stones, ny, nx)
    res = 0
    for i in range(nx):
        for j in range(ny):
            if stones[j][i] == ROUND:
                res += ny - j
    print(res)


def puzzle2():
    stones = get_stones()
    ny = len(stones)
    nx = len(stones[0])
    i = 0
    cache = {}

    score = str(stones)
    while score not in cache:
        cache[score] = i
        spin_cycle(stones, nx, ny)
        score = str(stones)
        i += 1

    lengh_loop = i - cache[score]
    start_loop = cache[score]
    remaining_cycles = (1000000000 - start_loop) % lengh_loop
    for k in range(remaining_cycles):
        spin_cycle(stones, nx, ny)

    res = 0
    for i in range(nx):
        for j in range(ny):
            if stones[j][i] == ROUND:
                res += ny - j
    print(res)


def get_stones():
    stones = []
    with open("input_14.txt", "r") as f:
        for ln in f:
            row_stone = [t for t in ln if t != '\n']
            stones.append(row_stone)
    return stones


puzzle1()
puzzle2()
