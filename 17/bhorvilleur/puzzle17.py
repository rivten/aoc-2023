import itertools

LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"
DOWN = "DOWN"
OPPOSITE = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}


class Pos:
    def __init__(self, x, y, d, steps):
        self.x = x
        self.y = y
        self.d = d
        self.steps = steps

    def __eq__(self, o: object) -> bool:
        if o is None:
            return False
        if not isinstance(o, Pos):
            return False
        return self.x == o.x and self.y == o.y and self.d == o.d and self.steps == o.steps

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.d, self.steps))

    def __str__(self) -> str:
        return str((self.x, self.y, self.d, self.steps))

    def __repr__(self) -> str:
        return str((self.x, self.y, self.d, self.steps))


def evaluate_path(loss_grid, old_pos, new_pos, least_loss, new_process):

    # Compute the value for the new position (if min_direction is higher than 1, we need to account for the value of
    # all the intermediary tiles)
    if new_pos.d == RIGHT:
        delta = sum([loss_grid[old_pos.x + 1 + dx, old_pos.y] for dx in range(new_pos.x - old_pos.x)])
    elif new_pos.d == DOWN:
        delta = sum([loss_grid[old_pos.x, old_pos.y + 1 + dy] for dy in range(new_pos.y - old_pos.y)])
    elif new_pos.d == LEFT:
        delta = sum([loss_grid[old_pos.x - 1 - dx, old_pos.y] for dx in range(old_pos.x - new_pos.x)])
    else:
        delta = sum([loss_grid[old_pos.x, old_pos.y - 1 - dy] for dy in range(old_pos.y - new_pos.y)])

    val = least_loss[old_pos.x, old_pos.y][old_pos] + delta
    # This value is to be stored only if we have not been able to reach the tile with a smaller value and in a
    # smaller number of last direction steps
    better_vals = [v for (p, v) in least_loss[(new_pos.x, new_pos.y)].items() if
                   p.d == new_pos.d and p.steps <= new_pos.steps and v < val]
    if len(better_vals) == 0:
        least_loss[(new_pos.x, new_pos.y)][new_pos] = val
        new_process.append(new_pos) # We add the new position in the remaining nodes so that it is processed in the
        # next iteration


def authorize_direction(pos, new_direction, max_direction):
    return pos.d != OPPOSITE[new_direction] \
        and (pos.d != new_direction or pos.steps < max_direction)


# The main Djistra iteration.
def process_neighbors(loss_grid, nx, ny, pos, least_loss, min_direction, max_direction):
    new_pos = []
    if ((pos.d == RIGHT and pos.x < nx - 1) or pos.x < nx - min_direction) \
            and authorize_direction(pos, RIGHT, max_direction):
        delta_steps = 1 if pos.d == RIGHT else min_direction
        new_steps = pos.steps + 1 if pos.d == RIGHT else min_direction
        evaluate_path(loss_grid, pos, Pos(pos.x + delta_steps, pos.y, RIGHT, new_steps), least_loss, new_pos)

    if ((pos.d == DOWN and pos.y < ny - 1) or pos.y < ny - min_direction) \
            and authorize_direction(pos, DOWN, max_direction):
        delta_steps = 1 if pos.d == DOWN else min_direction
        new_steps = pos.steps + 1 if pos.d == DOWN else min_direction
        evaluate_path(loss_grid, pos, Pos(pos.x, pos.y + delta_steps, DOWN, new_steps), least_loss, new_pos)

    if ((pos.d == LEFT and pos.x > 0) or pos.x >= min_direction) \
            and authorize_direction(pos, LEFT, max_direction):
        delta_steps = 1 if pos.d == LEFT else min_direction
        new_steps = pos.steps + 1 if pos.d == LEFT else min_direction
        evaluate_path(loss_grid, pos, Pos(pos.x - delta_steps, pos.y, LEFT, new_steps), least_loss, new_pos)

    if ((pos.d == UP and pos.y > 0) or pos.y >= min_direction) \
            and authorize_direction(pos, UP, max_direction):
        delta_steps = 1 if pos.d == UP else min_direction
        new_steps = pos.steps + 1 if pos.d == UP else min_direction
        evaluate_path(loss_grid, pos, Pos(pos.x, pos.y - delta_steps, UP, new_steps), least_loss, new_pos)

    return new_pos


def puzzle1():
    puzzle(1, 3)


def puzzle2():
    puzzle(4, 10)


# This main method computes and prints the least loss that the crucible should incur going from top-left to
# bottom-right. It implements a Djikstra algorithm where nodes corresponds to positions in the grid along with the
# direction of the crucible and the number of steps it has done in this direction.
# min_direction and max_direction are the minimum and maximum steps that one should go in one direction before turning.
def puzzle(min_direction, max_direction):
    loss_grid, nx, ny = get_loss_grid()

    # This variable is only for logging purposes
    solution = 9*nx * ny

    # The dictionary will give the least loss that the crucible should incur going from top-left to each tile of the grid.
    # For performance issues, it is first indexed by simple coordinates (x, y), then by direction and previous steps.
    least_loss = {}
    for x, y in itertools.product(range(nx), range(ny)):
        least_loss[(x, y)] = {}
    init_pos = Pos(0, 0, None, 0)
    least_loss[(init_pos.x, init_pos.y)][init_pos] = 0

    # The list of positions (nodes of the Djistra algorithm) that remains to process.
    to_process = set()
    to_process.add(init_pos)

    while len(to_process) > 0:
        new_to_process = []
        for p in to_process:
            new_to_process.extend(process_neighbors(loss_grid, nx, ny, p, least_loss, min_direction, max_direction))
        to_process = set(new_to_process)

        valid_vals = [val for (pos, val) in least_loss[(nx - 1, ny - 1)].items()]
        if len(valid_vals) > 0 and min(valid_vals) < solution:
            solution = min(valid_vals)
            print("New temporary solution : " + str(solution))


    print(solution)


def get_loss_grid():
    grid = {}
    ny = 0
    with open("input_17.txt", "r") as f:
        for j, ln in enumerate(f):
            for i, x in enumerate(ln):
                if x != '\n':
                    grid[(i, j)] = int(x)
            if ny == 0:
                nx = len([x for x in ln if x != '\n'])
            ny += 1
    return grid, nx, ny


puzzle1()
puzzle2()
