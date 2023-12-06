import math


def puzzle1():
    puzzle(False)


def puzzle2():
    puzzle(True)


def puzzle(only_one_race):
    res = 1
    times, distances = get_races(only_one_race)
    for i in range(len(times)):
        time = times[i]
        distance = distances[i]
        # Back in high school ! Trying to solve the equation : x² - time * x - distance > 0. Delta = b² - 4ac
        delta = time * time - 4 * distance
        # If delta < 0, it means that there is no way to reach the record (and that whoever did it probably cheated !)
        # If delta == 0, it means there is no way to break it, the record is already optimal.
        if delta <= 0:
            print("Infeasibility")
            return

        # Minimum time to press the button to break the record : x1 = (b - sqrt(delta)) / 2a
        first_valid_time = int((time - math.sqrt(delta)) / 2) + 1
        # Value beyond the maximum time to press the button to break the record : x2 = (b + sqrt(delta)) / 2a
        first_non_valid_time = math.ceil((time + math.sqrt(delta)) / 2)
        res = res * (first_non_valid_time - first_valid_time)
    print(res)


def get_races(only_one_race):
    with open("input_06.txt", "r") as f:
        time_line = f.readline()
        # If only_one_race is true, spaces will be deleted and the string read as one number
        if only_one_race:
            times = [int(time_line[time_line.index(":") + 1:].replace(" ", "").replace("\n", ""))]
        else:
            times = [int(t) for t in time_line[time_line.index(":") + 1:].split(" ") if t != '' and t != '\n']
        distance_line = f.readline()
        if only_one_race:
            distances = [int(distance_line[distance_line.index(":") + 1:].replace(" ", "").replace("\n", ""))]
        else:
            distances = [int(t) for t in distance_line[distance_line.index(":") + 1:].split(" ") if
                         t != '' and t != '\n']
    return times, distances


puzzle1()
puzzle2()
