def find_next(series):
    if len(set(series)) == 1:
        return series[0]

    diff = list(map(lambda a, b: a - b, series[1:], series[:-1]))
    next_diff = find_next(diff)
    return series[-1] + next_diff


def find_previous(series):
    if len(set(series)) == 1:
        return series[0]

    diff = list(map(lambda a, b: a - b, series[1:], series[:-1]))
    previous_diff = find_previous(diff)
    return series[0] - previous_diff


def puzzle1():
    series = get_series()
    for t in series:
        assert t[-1] == find_next(t[:-1])
    res = sum(find_next(t) for t in series)
    print(res)


def puzzle2():
    series = get_series()
    for t in series:
        assert t[-1] == find_next(t[:-1])
    res = sum(find_previous(t) for t in series)
    print(res)


def get_series():
    series = []
    with open("input_09.txt", "r") as f:
        for ln in f:
            series.append([int(t) for t in ln.split(" ")])
    return series


puzzle1()
puzzle2()
