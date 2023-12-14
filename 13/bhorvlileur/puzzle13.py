# Returns the number of differences between columns col1 and col2 in the given pattern.
def compare_columns(pattern, col1, col2):
    if col2 >= len(pattern[0]):
        return 0

    return len(set([i for i, row in enumerate(pattern) if row[col2] != row[col1]]))


# Returns the number of differences between rows row1 and row2 in the given pattern.
def compare_rows(pattern, row1, row2):
    if row2 >= len(pattern):
        return 0

    return len(set([i for i in range(len(pattern[row1])) if pattern[row1][i] != pattern[row2][i]]))


# Return the number (starting from 1) of the left position of the vertical mirror, or 0 if there is no vertical mirror.
def find_vertical_mirror(pattern, n_smudges):
    y = len(pattern[0])
    for i in range(y - 1):
        if sum([compare_columns(pattern, i - j, i + j + 1) for j in range(i + 1)]) == n_smudges:
            return i + 1
    return 0


# Return the number (starting from 1) of the upward position of the horizontal mirror, or 0 if there is no horizontal mirror.
def find_horizontal_mirror(pattern, n_smudges):
    x = len(pattern)
    for i in range(x - 1):
        if sum([compare_rows(pattern, i - j, i + j + 1) for j in range(i + 1)]) == n_smudges:
            return i + 1
    return 0


def puzzle(n_smudges):
    patterns = get_patterns()
    res = 0
    for pattern in patterns:
        hor = find_horizontal_mirror(pattern, n_smudges)
        ver = find_vertical_mirror(pattern, n_smudges)
        res += 100 * hor + ver
    print(res)


def puzzle1():
    puzzle(0)


def puzzle2():
    puzzle(1)


def get_patterns():
    patterns = []
    pattern = []
    with open("input_13.txt", "r") as f:
        for ln in f:
            if len(ln) == 1:
                patterns.append(pattern)
                pattern = []
            else:
                pattern.append([t for t in ln if t != '\n'])
        patterns.append(pattern)
    return patterns


puzzle1()
puzzle2()
