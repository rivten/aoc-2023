def puzzle1():
    res = 0
    with open("data_puzzle.txt", "r") as f:
        for ln in f:
            _, first_digit, _, last_digit = read_digits_puzzle(ln)
            res = res + 10 * first_digit + last_digit
    print(res)


def puzzle2():
    res = 0
    script_numbers = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
                      "nine": 9}
    with open("data_puzzle.txt", "r") as f:
        for ln in f:
            pos_first_digit, first_digit, pos_last_digit, last_digit = read_digits_puzzle(ln)

            for script_digit, digit in script_numbers.items():
                pos = ln.find(script_digit)
                if pos != -1 and pos < pos_first_digit:
                    pos_first_digit = pos
                    first_digit = digit
                pos = ln.rfind(script_digit)
                if pos != -1 and pos > pos_last_digit:
                    pos_last_digit = pos
                    last_digit = digit
            value_line = 10 * first_digit + last_digit
            res = res + value_line
    print(res)


def read_digits_puzzle(ln):
    first_digit = None
    last_digit = None
    pos_first_digit = len(ln)
    pos_last_digit = 0
    for i in range(len(ln)):
        if ln[i].isdigit():
            last_digit = ln[i]
            pos_last_digit = i
            if first_digit is None:
                first_digit = ln[i]
                pos_first_digit = i
    return pos_first_digit, int(first_digit), pos_last_digit, int(last_digit)


puzzle1()
puzzle2()
