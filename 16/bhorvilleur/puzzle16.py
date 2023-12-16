LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"
DOWN = "DOWN"
VERTICAL_SPLITTER = '|'
HORIZONTAL_SPLITTER = '-'
NORTH_WEST_MIRROR = '/'
NORTH_EAST_MIRROR = '\\'
NORTH_WEST_MIRROR_SWITCH = {LEFT: DOWN, DOWN: LEFT, UP: RIGHT, RIGHT: UP}
NORTH_EAST_MIRROR_SWITCH = {LEFT: UP, UP: LEFT, DOWN: RIGHT, RIGHT: DOWN}


# Find the next position in the grid given the direction
def advance(pos_x, pos_y, direction):
    if direction == LEFT:
        return pos_x - 1, pos_y
    if direction == RIGHT:
        return pos_x + 1, pos_y
    if direction == UP:
        return pos_x, pos_y - 1
    if direction == DOWN:
        return pos_x, pos_y + 1


# Find the next direction(s) in the grid given the previous direction and the current tile.
# Mirrors are reflecting the direction, SPLITTERS are splitting when taken orthogonally.
def update_direction(direction, tile):
    if tile == VERTICAL_SPLITTER and (direction == LEFT or direction == RIGHT):
        return [UP, DOWN]
    if tile == HORIZONTAL_SPLITTER and (direction == UP or direction == DOWN):
        return [LEFT, RIGHT]
    if tile == NORTH_WEST_MIRROR:
        return [NORTH_WEST_MIRROR_SWITCH[direction]]
    if tile == NORTH_EAST_MIRROR:
        return [NORTH_EAST_MIRROR_SWITCH[direction]]
    return [direction]


# Follow a beam from a starting position in a certain direction, until it hurts a mirror or a splitter, or get out
# of the grid. If the beam hurts a mirror or splitter, then the subsequent beams (position and directions) are returned.
# The "light" set if filled with all the position encountered.
def follow_beam(grid, lights, nx, ny, init_pos_x, init_pos_y, direction):
    pos_x, pos_y = init_pos_x, init_pos_y

    while 0 <= pos_x < nx and 0 <= pos_y < ny and not (pos_x, pos_y) in grid:
        lights.add((pos_x, pos_y))
        (pos_x, pos_y) = advance(pos_x, pos_y, direction)

    new_beams = []
    if (pos_x, pos_y) in grid:
        lights.add((pos_x, pos_y))
        new_directions = update_direction(direction, grid[(pos_x, pos_y)])
        for new_direction in new_directions:
            new_pos_x, new_pos_y = advance(pos_x, pos_y, new_direction)
            if 0 <= new_pos_x < nx and 0 <= new_pos_y < ny:
                new_beams.append((new_pos_x, new_pos_y, new_direction))

    return new_beams


# Find the number of tiles encountered by a series of beams starting a certain position and direction in the grid.
def find_number_of_energized_tiles(grid, nx, ny, init_x, init_y, direction):
    lights = set()
    beams = [(init_x, init_y, direction)]  # The list of beams to process
    processed_beams = set()  # To avoid infinite loops, we store the already processed beams so that we don't process
    # them again.
    while len(beams) != 0:
        new_beams = []
        for beam in beams:
            (pos_x, pos_y, direction) = beam
            new_beams.extend(follow_beam(grid, lights, nx, ny, pos_x, pos_y, direction))
            processed_beams.add(beam)
        beams = [beam for beam in new_beams if beam not in processed_beams]
    return len(lights)


def puzzle1():
    grid, nx, ny = get_grid()
    print(find_number_of_energized_tiles(grid, nx, ny, 0, 0, RIGHT))


def puzzle2():
    grid, nx, ny = get_grid()
    res = 0

    for i in range(nx):
        n = find_number_of_energized_tiles(grid, nx, ny, i, 0, DOWN)
        res = max(n, res)
        n = find_number_of_energized_tiles(grid, nx, ny, i, ny - 1, UP)
        res = max(n, res)
    for j in range(ny):
        n = find_number_of_energized_tiles(grid, nx, ny, 0, j, RIGHT)
        res = max(n, res)
        n = find_number_of_energized_tiles(grid, nx, ny, nx - 1, j, LEFT)
        res = max(n, res)

    print(res)


def get_grid():
    grid = {}
    ny = 0
    with open("input_16.txt", "r") as f:
        for j, ln in enumerate(f):
            for i, x in enumerate(ln):
                if x in [HORIZONTAL_SPLITTER, VERTICAL_SPLITTER, NORTH_WEST_MIRROR, NORTH_EAST_MIRROR]:
                    grid[(i, j)] = x
            if ny == 0:
                nx = len([x for x in ln if x != '\n'])
            ny += 1
    return grid, nx, ny


puzzle1()
puzzle2()
