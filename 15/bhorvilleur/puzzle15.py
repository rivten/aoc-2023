def puzzle1():
    sequence = get_sequence()
    res = sum([get_hash(string, 256) for string in sequence])
    print(res)


def get_hash(string, size_hash):
    res = 0
    for ch in string:
        res += ord(ch)
        res = (res * 17) % size_hash
    return res


class Hashmap:

    def __init__(self, size_hash):
        self.size_hash = size_hash
        self.boxes = [([], []) for _ in range(size_hash)]

    def remove(self, label):
        lenses, values = self.boxes[get_hash(label, self.size_hash)]
        if label in lenses:
            i = lenses.index(label)
            lenses.pop(i)
            values.pop(i)

    def put(self, label, value):
        lenses, values = self.boxes[get_hash(label, self.size_hash)]
        if label in lenses:
            i = lenses.index(label)
            values[i] = value
        else:
            lenses.append(label)
            values.append(value)

    def get_power(self):
        res = 0
        for i, (_, values) in enumerate(self.boxes):
            for j, value in enumerate(values):
                j_value = (i + 1) * (j + 1) * value
                res += j_value
        return res


def puzzle2():
    sequence = get_sequence()
    hashmap = Hashmap(256)
    for operation in sequence:
        if "=" in operation:
            label = operation[:operation.index("=")]
            value = int(operation[operation.index("=") + 1:])
            hashmap.put(label, value)
        elif "-" in operation:
            label = operation[:operation.index("-")]
            hashmap.remove(label)
        else:
            print("Error")
    print(hashmap.get_power())


def get_sequence():
    with open("input_15.txt", "r") as f:
        sequence = f.readline().split(",")
    return sequence


puzzle1()
puzzle2()
