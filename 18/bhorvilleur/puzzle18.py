UP, DOWN, LEFT, RIGHT = "U", "D", "L", "R"
DIRECTIONS = "RDLU"
REVERSE = {LEFT: RIGHT, RIGHT: LEFT}

VERTICAL = '|'
HORIZONTAL = '-'
WEST = 0
EAST = 1


def puzzle1():
    puzzle(False)


def puzzle2():
    puzzle(True)


def puzzle(reverse_plan):
    lines, (init_pos_x, init_pos_y) = get_dig_plan(reverse_plan)
    vertical_bars = compute_vertical_bars(lines, init_pos_x, init_pos_y) # Transform data in a set of "vertical bars"
    print(get_total_number_of_inner_tiles(vertical_bars))

# Transform the raw data in a set of undirected "vertical bar". A vertical bar corresponds to a move up or down.
# It is defined by its horizontal coordinate (x) and vertical extremities (y0 and y), as well as the direction of the
# loop at these extremities (left if the horizontal bar is left to the vertical bar, right otherwise (independently of
# whether the horizontal bar was "going" left or right in the loop).
# Vertical bars are then grouped by their x coordinate.
def compute_vertical_bars(lines, init_pos_x, init_pos_y):
    vertical_bars = {} # Dictionary giving the sets of vertical bar by x coordinate.

    x0, y0 = (init_pos_x, init_pos_y)   # We start the loop at its first move
    x, y = x0, y0
    for (direction_p, _), (direction, distance), (direction_s, _) in zip([lines[-1]] + lines[:-1], lines,
                                                                         lines[1:] + [lines[0]]):
        # direction_p is the previous direction, direction is the current direction, direction_n is the next direction.
        # if direction is up or down, we will register the vertical bar.
        if direction == DOWN:
            y = y0 + distance
            if x not in vertical_bars:
                vertical_bars[x] = []
            vertical_bars[x].append((y0, y, REVERSE[direction_p], direction_s))
        if direction == UP:
            y = y0 - distance
            if x not in vertical_bars:
                vertical_bars[x] = []
            vertical_bars[x].append((y, y0, direction_s, REVERSE[direction_p]))
        if direction == RIGHT:
            x = x0 + distance
        if direction == LEFT:
            x = x0 - distance
        x0, y0, = x, y

    return sorted(vertical_bars.items()) # We sort the x coordinates

# Given a set of vertical bar, this method will count the number of inner points, by iterating column by columns.
def get_total_number_of_inner_tiles(vertical_bars):
    horizontal_bars = [] # At each point, we save the sorted positions of the current horizontal bar
    xp = 0 # This will store the previous x coordinate containing at least one vertical bar
    res = 0 # This will store the total number of inner tiles

    for (x, vertical_bars_x) in vertical_bars: # Looping on x coordinates containing vertical bars
        if x > xp + 1: # If there is at least one x coordinate not containing any vertical bars since the last iteration
            # We count the number of inner points (only considering horizontal bars), multiplying it by the number of
            # x-coordinates that presents the same horizontal bars
            res = res + get_inner_tiles(list(horizontal_bars)) * (x - xp - 1)

        # Now, we are reconstituting the column for the x coordinate
        column = []
        new_horizontal_bars = []
        for (y0, y1, d0, d1) in vertical_bars_x: # Looping on the vertical bars of the x-coordinate
            column.append((y0, VERTICAL, (y1, d0 != d1)))
            # For each of the extremities, we check if it is located at the left or the right of the vertical bar.
            # If it is on the left, it corresponds to the end of a extant horizontal bar (that needs to be removed)
            # If it is on the right, it corresponds to the beginning of a new horizontal bar (that needs to be added)
            # Note : these new horizontal bars will be added after counting the number of inner tiles of the column
            if d0 == LEFT:
                horizontal_bars.remove((y0, HORIZONTAL, 0))
            else:
                new_horizontal_bars.append((y0, HORIZONTAL, 0))
            if d1 == LEFT:
                horizontal_bars.remove((y1, HORIZONTAL, 0))
            else:
                new_horizontal_bars.append((y1, HORIZONTAL, 0))

        # Merge and sort the horizontal and vertical bars encountered by the column
        column.extend(horizontal_bars)
        column = sorted(column)
        # Compute the number of inner tiles for the column
        res += get_inner_tiles(column)

        # dd the new horizontal tile to the extant one, and sort the result
        horizontal_bars = sorted(horizontal_bars + new_horizontal_bars)
        xp = x

    return res


def get_inner_tiles(column):
    number_inside = 0

    inside = False  # We start at y = -1, outside the loop
    yp = -1
    for (y, t, l) in column:

        if inside:
            number_inside += y - yp - 1
        # loop to outside
        if t == HORIZONTAL:  # Horizontal pipe : we go one step forward and we cross a border
            border_crossing = True
            number_inside += 1
            yp = y
        else:  # Vertical pipes : we advance a number of steps equals to the size of the pipe.
            yp, border_crossing = l
            number_inside += 1 + yp - y
        # If there is a border crossing, we switch the variable inside.
        if border_crossing:
            inside = not inside

    assert inside is False
    return number_inside


def get_dig_plan(reverse_infos):
    lines = []
    x_min, y_min = 0, 0
    x, y = 0, 0
    with open("input_18.txt", "r") as f:
        for ln in f:
            if reverse_infos:  # puzzle 2 : read the "color" field
                direction = DIRECTIONS[int(ln[ln.index("#") + 6])]
                distance = int(ln[ln.index("#") + 1:ln.index("#") + 6], 16)
            else:  # puzzle 1
                direction = ln[0]
                distance = int(ln.split(" ")[1])
            lines.append((direction, distance))
            if direction == LEFT:
                x -= distance
                x_min = min(x, x_min)
            if direction == RIGHT:
                x += distance
            if direction == UP:
                y -= distance
                y_min = min(y, y_min)
            if direction == DOWN:
                y += distance
    assert (x, y) == (0, 0) # Check that we have done a loop
    return lines, (-x_min, -y_min)


puzzle1()
puzzle2()
