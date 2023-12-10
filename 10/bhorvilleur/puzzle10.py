VERTICAL = '|'
HORIZONTAL = '-'
NORTH_EAST = 'L'
NORTH_WEST = 'J'
SOUTH_WEST = '7'
SOUTH_EAST = 'F'
START = "S"
WEST = 0
EAST = 1


def find_next_position(x, y, xp, yp, shape):
    if shape == HORIZONTAL:
        if yp != y:
            return -1, -1
        x = x + 1 if xp == x - 1 else x - 1
        y = y
    elif shape == VERTICAL:
        if xp != x:
            return -1, -1
        x = x
        y = y + 1 if yp == y - 1 else y - 1
    elif shape == NORTH_EAST:
        if (xp, yp) != (x + 1, y) and (xp, yp) != (x, y - 1):
            return -1, -1
        x = x + 1 if xp == x else x
        y = y - 1 if yp == y else y
    elif shape == NORTH_WEST:
        if (xp, yp) != (x - 1, y) and (xp, yp) != (x, y - 1):
            return -1, -1
        x = x - 1 if xp == x else x
        y = y - 1 if yp == y else y
    elif shape == SOUTH_EAST:
        if (xp, yp) != (x + 1, y) and (xp, yp) != (x, y + 1):
            return -1, -1
        x = x + 1 if xp == x else x
        y = y + 1 if yp == y else y
    else:
        if (xp, yp) != (x - 1, y) and (xp, yp) != (x, y + 1):
            return -1, -1
        x = x - 1 if xp == x else x
        y = y + 1 if yp == y else y
    return x, y


def find_loop(pipes, start_pos, start_shape):
    xs, ys = start_pos
    shape = start_shape
    x, y = xs, ys

    if shape in [VERTICAL, SOUTH_WEST, SOUTH_EAST]:
        xt, yt = x, y + 1
    elif shape in [HORIZONTAL, NORTH_WEST]:
        xt, yt = x - 1, y
    else:
        xt, yt = x + 1, y
    if (xt, yt) not in pipes:
        return None

    xp, yp = xt, yt
    loop = []
    while len(loop) == 0 or (x, y) != (xs, ys) or (xp, yp) != (xt, yt):
        x1, y1 = find_next_position(x, y, xp, yp, shape)
        if (x1, y1) not in pipes:
            return None
        xp, yp = x, y
        x, y = x1, y1
        shape = pipes[x, y]
        loop.append((x, y))
    return loop


def puzzle1():
    pipes, start_pos = get_pipes()
    for start_shape in [VERTICAL, HORIZONTAL, NORTH_EAST, NORTH_WEST, SOUTH_WEST, SOUTH_EAST]:
        loop = find_loop(pipes, start_pos, start_shape=start_shape)
        if loop is not None:
            print(start_shape + " " + str(len(loop) // 2))

# Strategy for puzzle 2 (counting the number of blocks inside the loop) :
# We will go through all columns of the grid, and determine at each point if we are inside or outside the loop
def puzzle2():
    pipes, start_pos = get_pipes()
    for start_shape in [VERTICAL, HORIZONTAL, NORTH_EAST, NORTH_WEST, SOUTH_WEST, SOUTH_EAST]:
        loop = find_loop(pipes, start_pos, start_shape=start_shape)
        if loop is not None:
            break
    n = max([x for (x, _) in loop]) + 1
    m = max([y for (_, y) in loop]) + 1

    number_inside = 0

    for x in range(n):
        inside = False
        coming_from = None
        for y in range(m):
            if (x, y) in loop:
                border_crossing = False # Will be set to true if going through this block make you go from inside the
                # loop to ouside
                if pipes[(x, y)] == VERTICAL: # Vertical pipes never make you go from inside to outside
                    pass
                elif pipes[(x, y)] == HORIZONTAL: # Horizontal pipes always make you go from inside to outside
                    border_crossing = True
                # If we see a south-west/east pipe, we assume there is going to be a north-west/east pipe below.
                # It will count as a border crossing if and only if the two pipes come from different directions
                # For now we just save the direction of the pipe in the variable coming_from
                elif pipes[(x, y)] == SOUTH_EAST:
                    coming_from = EAST
                elif pipes[(x, y)] == SOUTH_WEST:
                    coming_from = WEST
                # Once we see the north-west/east, we can determine if this corresponds to a border crossing
                elif pipes[(x, y)] == NORTH_EAST:
                    border_crossing = (coming_from == WEST)
                else:
                    border_crossing = (coming_from == EAST)

                # If there is a border crossing, we switch the variable inside.
                if border_crossing:
                    inside = not inside

            elif inside:
                # If we are inside, we increment the number of inside visited blocks
                number_inside += 1
        assert inside is False
    print(number_inside)


def get_pipes():
    pipes = {}
    with open("input_10.txt", "r") as f:
        for (y, ln) in enumerate(f):
            for (x, t) in enumerate(ln):
                if t in [HORIZONTAL, VERTICAL, NORTH_EAST, NORTH_WEST, SOUTH_WEST, SOUTH_EAST, START]:
                    pipes[(x, y)] = t
                if t == START:
                    start = (x, y)
    return pipes, start


puzzle1()
puzzle2()
