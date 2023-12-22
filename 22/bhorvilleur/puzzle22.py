import itertools
from copy import deepcopy

# Find the position of each brick once it is fallen, and fill the information in the fallen_bricks map.
def fall(brick_num, bricks, fallen_bricks, below_bricks):
    if brick_num in fallen_bricks: # Cache to avoid a complexity explosion
        return

    # Compute recursively the position of any brick below
    zmin = 0
    for below_brick in below_bricks[brick_num]:
        fall(below_brick, bricks, fallen_bricks, below_bricks)
        zmin = max(zmin, fallen_bricks[below_brick][1][2])

    # The bottom position of the brick is the max of the top position of all the bricks below, plus one
    zmin = zmin + 1
    (x0, y0, z0), (x1, y1, z1) = bricks[brick_num]
    assert zmin <= z0

    fallen_brick = (x0, y0, zmin), (x1, y1, zmin + z1 - z0)
    fallen_bricks[brick_num] = fallen_brick

# For each (x, y) column, list all the bricks that compose the column, with their min and max z-coordinate.
def analyse_columns(xmax, ymax, bricks):
    columns = {}

    for i, j in itertools.product(range(xmax + 1), range(ymax + 1)):
        columns[(i, j)] = []

    for k, ((x0, y0, z0), (x1, y1, z1)) in bricks.items():
        if z0 < z1:  # Vertical block
            columns[(x0, y0)].append((z0, z1, k))
        elif x0 < x1:
            for dx in range(x1 - x0 + 1):
                columns[(x0 + dx, y0)].append((z0, z0, k))
        else:
            for dy in range(y1 - y0 + 1):
                columns[(x0, y0 + dy)].append((z0, z0, k))

    return columns

# Take the bricks snapshot and returns maps indicating which bricks are on top of each other.
def compute_support_relations(xmax, ymax, bricks):

    # First column analysis (on the snapshot)
    columns = analyse_columns(xmax, ymax, bricks)

    # Look through all columns to find out which bricks are on top of each other in the snapshot
    below_bricks = {t: set() for t in range(len(bricks))}
    for column in columns.values():
        col = sorted(column)
        for (_, _, k1), (_, _, k2) in zip(col[:-1], col[1:]):
            below_bricks[k2].add(k1)

    # Now that the below relationships are determined in the snapshot, we can compute the position of the fallen bricks
    fallen_bricks = {}
    for brick_num in bricks.keys():
        fall(brick_num, bricks, fallen_bricks, below_bricks)

    # Second column analysis (on the fallen bricks)
    fallen_columns = analyse_columns(xmax, ymax, fallen_bricks)

    # Look through all columns to find out which fallen bricks are on top of each other
    below_bricks = {t: set() for t in range(len(bricks))}
    above_bricks = {t: set() for t in range(len(bricks))}

    for column in fallen_columns.values():
        col = sorted(column)
        for (z10, z11, k1), (z20, z21, k2) in zip(col[:-1], col[1:]):
            if z20 == z11 + 1:
                below_bricks[k2].add(k1)
                above_bricks[k1].add(k2)
    return below_bricks, above_bricks


def puzzle1():
    # Parse data
    (_, xmax), (_, ymax), (_, _), bricks = get_bricks()

    # Compute the graph of which bricks are on top of each other
    below_bricks, above_bricks = compute_support_relations(xmax, ymax, bricks)

    # Find out the disintegratable bricks : they are the one that has either no bricks above, or whose above bricks
    # are supported by at least another bricks
    number_of_disintegratable_bricks = 0
    for brick, above_bricks in above_bricks.items():
        disintegratable = True
        for above_brick in above_bricks:
            if len(below_bricks[above_brick]) == 1:
                disintegratable = False
        if disintegratable:
            number_of_disintegratable_bricks += 1
    print(number_of_disintegratable_bricks)

#
def get_chain_reaction(brick_num, above_bricks, below_bricks):

    # We make a copy of the below_bricks map and remove the bricks in it as the chain reaction goes.
    new_below_bricks = deepcopy(below_bricks)

    chain_reaction = set()
    bricks_to_remove = {brick_num}

    while len(bricks_to_remove) != 0:
        brick_to_remove = bricks_to_remove.pop()
        for above_brick in above_bricks[brick_to_remove]:
            new_below_bricks[above_brick].remove(brick_to_remove)
            if len(new_below_bricks[above_brick]) == 0:
                chain_reaction.add(above_brick)
                bricks_to_remove.add(above_brick)

    return len(chain_reaction)


def puzzle2():
    (_, xmax), (_, ymax), (_, _), bricks = get_bricks()
    below_bricks, above_bricks = compute_support_relations(xmax, ymax, bricks)

    total_chain_reactions = 0
    for brick in bricks.keys():
        total_chain_reactions += get_chain_reaction(brick, above_bricks, below_bricks)
    print(total_chain_reactions)


def get_bricks():
    bricks = {}
    xmin, xmax, ymin, ymax, zmin, zmax = None, None, None, None, None, None
    with open("input_22.txt", "r") as f:
        for (i, ln) in enumerate(f):
            pos0 = tuple([int(t) for t in ln[:ln.index('~')].split(",")])
            pos1 = tuple([int(t) for t in ln[ln.index('~') + 1:].replace('\n', '').split(",")])
            bricks[i] = pos0, pos1
            assert pos0[0] <= pos1[0]
            assert pos0[1] <= pos1[1]
            assert pos0[2] <= pos1[2]
            assert (pos1[0] - pos0[0]) * (pos1[1] - pos0[1]) == 0
            assert (pos1[0] - pos0[0]) * (pos1[2] - pos0[2]) == 0
            assert (pos1[1] - pos0[1]) * (pos1[2] - pos0[2]) == 0
            xmin = min(xmin, pos0[0]) if xmin is not None else pos0[0]
            xmax = max(xmax, pos1[0]) if xmax is not None else pos1[0]
            ymin = min(ymin, pos0[1]) if ymin is not None else pos0[1]
            ymax = max(ymax, pos1[1]) if ymax is not None else pos1[1]
            zmin = min(zmin, pos0[2]) if zmin is not None else pos0[2]
            zmax = max(zmax, pos1[2]) if zmax is not None else pos1[2]

    return (xmin, xmax), (ymin, ymax), (zmin, zmax), bricks


puzzle1()
puzzle2()
