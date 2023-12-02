import numpy

red = "red"
green = "green"
blue = "blue"


def puzzle1(maxRed, maxGreen, maxBlue):
    limits = {red: maxRed, green: maxGreen, blue: maxBlue}

    def compute(id, drawings):
        is_ok = all(all((value <= limits[color]) for (color, value) in drawing.items()) for drawing in drawings)
        return id if is_ok else 0

    processFile(compute)


def puzzle2():
    def compute(id, drawings):
        return numpy.prod([max(drawing[color] for drawing in drawings if color in drawing) for color in [red, green, blue]])

    processFile(compute)


def processFile(compute_method):
    res = 0
    with open("input_02.txt", "r") as f:
        for ln in f:
            pos_id_game = len("Game")
            pos_colon = ln.find(": ")
            id = int(ln[pos_id_game:pos_colon])
            str_drawings = ln[pos_colon + 2:].replace("\n", "").split("; ")
            drawings = []
            for str_drawing in str_drawings:
                colors = str_drawing.split(", ")
                drawing = {}
                for color in colors:
                    pos_space = color.find(" ")
                    color_name = color[pos_space + 1:]
                    value = int(color[:pos_space])
                    drawing[color_name] = value
                drawings.append(drawing)
            res = res + compute_method(id, drawings)
    print(res)


puzzle1(12, 13, 14)
puzzle2()
