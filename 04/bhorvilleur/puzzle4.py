def puzzle1():
    matching_number_per_card = get_matching_cards()
    print(sum(pow(2, t-1) for t in matching_number_per_card if t > 0))



def puzzle2():
    matching_number_per_card = get_matching_cards()
    n = len(matching_number_per_card)
    number_per_card = []
    for i in range(n):
        number_per_card.append(1 + sum(number_per_card[i-matching_number_per_card[n-i-1]:]))
    print(sum(number_per_card))

def get_matching_cards():
    matching_number_per_cards = []
    with open("input_04.txt", "r") as f:
        for ln in f:
            str_winning = ln[ln.find(":") + 2:ln.find("|")]  # +2 to avoid the first space
            str_played = ln[ln.find("|") + 2:]
            winning_numbers = [int(t) for t in str_winning.split(" ") if t != '']
            played_numbers = [int(t) for t in str_played.split(" ") if t != '']
            matching_number_per_cards.append(len([t for t in winning_numbers if t in played_numbers]))
    return matching_number_per_cards
puzzle1()
puzzle2()
