def puzzle1():
    puzzle(get_score_puzzle_1)


def puzzle2():
    puzzle(get_score_puzzle_2)


def puzzle(get_score_func):
    cards = get_cards()
    cards_by_score = sorted((get_score_func(k), v) for (k, v) in cards.items())
    result = sum((i + 1) * bet for (i, (_, bet)) in enumerate(cards_by_score))
    print(result)


def get_score_puzzle_1(combination: str):
    occurrences = sorted([combination.count(k) for k in set(combination)])
    cards = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    if occurrences == [5]:
        type = 6
    elif occurrences == [1, 4]:
        type = 5
    elif occurrences == [2, 3]:
        type = 4
    elif occurrences == [1, 1, 3]:
        type = 3
    elif occurrences == [1, 2, 2]:
        type = 2
    elif occurrences == [1, 1, 1, 2]:
        type = 1
    else:
        type = 0

    score = type
    for k in combination:
        score = 15 * score + cards.index(k)
    return score


def get_score_puzzle_2(combination: str):
    occurrences = sorted([combination.count(k) for k in set(combination) if k != 'J'])
    cards = ['J', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
    if len(occurrences) <= 1:  # Only one color, or zero -> five of a kind
        type = 6
    elif len(occurrences) == 2 and occurrences[0] == 2:  # Only 2 colors, with at least two pairs -> full house
        type = 4
    elif len(occurrences) == 2:  # Only 2 colors, possibility to go to four of a kind
        type = 5
    elif len(occurrences) == 3 and occurrences[1] == 1:  # 3 colors, two of them unique -> three of a kind
        type = 3
    elif len(occurrences) == 3:  # 3 colors, at least two pairs -> two pairs
        type = 2
    elif len(occurrences) == 4:  # 4 colors -> one pair
        type = 1
    else:
        type = 0

    score = type
    for k in combination:
        score = 15 * score + cards.index(k)
    return score


def get_cards():
    cards = dict()
    with open("input_07.txt", "r") as f:
        for ln in f:
            cards[ln[:ln.index(" ")]] = int(ln[ln.index(" ") + 1:len(ln)].replace("\n", ""))
    return cards


puzzle1()
puzzle2()
