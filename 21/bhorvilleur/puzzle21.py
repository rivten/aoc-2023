def walk_one_step(nx, ny, rocks, pos):
    new_pos = set()
    for (x, y) in pos:
        if x < nx - 1 and (x + 1, y) not in rocks:
            new_pos.add((x + 1, y))
        if y < ny - 1 and (x, y + 1) not in rocks:
            new_pos.add((x, y + 1))
        if x > 0 and (x - 1, y) not in rocks:
            new_pos.add((x - 1, y))
        if y > 0 and (x, y - 1) not in rocks:
            new_pos.add((x, y - 1))

        if x == 0 and (nx - 1, y) not in rocks:
            new_pos.add((nx - 1, y))
        if y == 0 and (x, ny - 1) not in rocks:
            new_pos.add((x, ny - 1))
        if x == nx - 1 and (0, y) not in rocks:
            new_pos.add((0, y))
        if y == ny - 1 and (x, 0) not in rocks:
            new_pos.add((x, 0))
    return new_pos


def get_grid():
    rocks = []
    starting_pos = (0, 0)
    ny = 0
    with open("input_21.txt", "r") as f:
        for j, ln in enumerate(f):
            for i, x in enumerate(ln):
                if x == '#':
                    rocks.append((i, j))
                elif x == 'S':
                    starting_pos = (i, j)
            if ny == 0:
                nx = len([x for x in ln if x != '\n'])
            ny += 1
    return rocks, starting_pos, nx, ny


def puzzle1():
    rocks, init_pos, nx, ny = get_grid()
    pos = [init_pos]
    for i in range(1000):
        print(len(pos))
        pos = walk_one_step(nx, ny, rocks, pos)
    print(len(pos))


def puzzle2():
    rocks, starting_pos, nx, ny = get_grid()



puzzle1()
# puzzle2()
