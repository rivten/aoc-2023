VALID = '.'
DEFECTIVE = '#'
UNKNOWN = '?'

# Find the number of combinations that match the given list o springs and defective_rows, from i_spring and i_def_row
# positions.
# springs : the array of springs, containing SAFE, DEFECTIVE and UNKNOWN symbols
# defective_rows : the list of consecutive defective rows
# i_spring : the starting index of the array springs to consider
# i_def_row : the starting index of the array defective_rows to consider
# cache : a dictionary of the already visited couples i_spring/i_def_row. This cache avoids a complexity explosion.
def find_combinations(springs, defective_rows, i_spring, i_def_row, cache):

    # Check the cache : if the couple (i_spring, i_def_row) has already been visited, no need to go further
    if (i_spring, i_def_row) in cache:
        return cache[(i_spring, i_def_row)]

    # If we are at the end of the springs array, there is one solution if and only if there is no more defective rows
    # to consider.
    if i_spring == len(springs):
        res = 1 if i_def_row == len(defective_rows) else 0
        cache[(i_spring, i_def_row)] = res
        return res

    # Hypothesis 1 : the next spring is VALID
    res = 0
    if springs[i_spring] != DEFECTIVE:
        res += find_combinations(springs, defective_rows, i_spring + 1, i_def_row, cache)

    # Hypothesis 2 : the next spring is DEFECTIVE (only works if there is at least one more defective_row to consider)
    if springs[i_spring] != VALID and i_def_row < len(defective_rows):
        n_row_defective = defective_rows[i_def_row]
        # Check that there is at least n more springs to consider and that these springs are defective (or unknown)
        if i_spring + n_row_defective > len(springs) or len(
                [t for t in springs[i_spring + 1:i_spring + n_row_defective] if t == VALID]) > 0:
            pass
        # If we reached the end of the spring array : we must also have reached the end of the defective_row array
        elif i_spring + n_row_defective == len(springs):
            res += 1 if i_def_row + 1 == len(defective_rows) else 0
        # Otherwise, we check that the following spring is valid (or unknwown)
        elif springs[i_spring + n_row_defective] == DEFECTIVE:
            pass
        else:
            res += find_combinations(springs, defective_rows, i_spring + n_row_defective + 1, i_def_row + 1, cache)

    # Filling cache
    cache[(i_spring, i_def_row)] = res
    return res


def puzzle1():
    data = getData()
    res = sum([find_combinations(springs, defectiveRows, 0, 0, {}) for springs, defectiveRows in data])
    print(res)


def duplicate(springs, defective_rows, n):
    new_springs, new_defective_rows = [],[]
    for i in range(n):
        if i > 0:
            new_springs.append(UNKNOWN)
        new_springs.extend(springs)
        new_defective_rows.extend(defective_rows)
    return new_springs, new_defective_rows


def puzzle2():
    data = getData()
    res = 0
    for (springs, defectiveRows) in data:
        new_springs, new_defectiveRows = duplicate(springs, defectiveRows, 5)
        combinations = find_combinations(new_springs, new_defectiveRows, 0, 0, {})
        res += combinations
    print(res)


def getData():
    data = []
    with open("input_12.txt", "r") as f:
        for ln in f:
            sep = ln.index(" ")
            springs = [t for t in ln[:sep]]
            defectiveRows = [int(t) for t in ln[sep + 1:].split(",")]
            data.append((springs, defectiveRows))
    return data


puzzle1()
puzzle2()
