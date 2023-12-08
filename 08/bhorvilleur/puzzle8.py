import itertools


def puzzle1():
    directions, network = get_map()
    pos_direction = 0
    pos_network = 'AAA'
    n = 0
    while pos_network != 'ZZZ':
        if directions[pos_direction] == 'L':
            pos_network = network[pos_network][0]
        else:
            pos_network = network[pos_network][1]
        pos_direction = (pos_direction + 1) % len(directions)
        n = n + 1
    print(n)


# This class serves only for puzzle 2. It models a pathway (starting with a "__A" node) by the indexes that ends with
# Z ("__Z"), the first index of the loop, and the size of the loop.
class Pathway:
    def __init__(self, start_loop, length_loop, stops):
        self.start_loop = start_loop
        self.loop_length = length_loop
        self.stops = stops

    def concat(self, other):
        if len(self.stops) == 0:
            return other
        new_start_loop = max(self.start_loop, other.start_loop)
        l1 = self.loop_length
        l2 = other.loop_length
        # Bezout identity : u * l1 + v * l2 = g (1), with g being the GCD of l1 and l2 (the former length)
        (g, u, v) = extended_euclidian(l1, l2)

        # The new loop length is the LCM of the former lengths
        new_loop_length = l1 * l2 // g

        stops = []

        # Though in the input data, each starting point is only linked to an only end point, we still take into
        # account the possibility that the pathway present several "stops"
        for (stop1, stop2) in itertools.product(self.stops, other.stops):
            # First we remove the part that is before the loop starting point (assuming the stops are not before it)
            t1 = stop1 - new_start_loop
            t2 = stop2 - new_start_loop
            # We are trying to find x and y such as t1 + x*l1 = t2 + y*l2.
            # That is : x * l1 - y * l2 = (t1 - t2). (2)
            # Bezout identity tells us that this can only be if (t2 - t1) is a multiple of the GDC of l1 and l2
            if (t2 - t1) % g != 0:
                continue  # We can never be simultaneously on t1 and t2

            k = (t2 - t1) // g
            # Confronting (1) and (2), we can determine that x1 is congruent to u*k, modulus the new length
            t = (t1 + u * l1 * k) % new_loop_length
            stop = new_start_loop + t
            stops.append(stop)
        return Pathway(new_start_loop, new_loop_length, list(sorted(stops)))


def extended_euclidian(a, b):
    r, u, v, r2, u2, v2 = a, 1, 0, b, 0, 1
    while r2 != 0:
        q = r // r2
        r, u, v, r2, u2, v2 = r2, u2, v2, r - q * r2, u - q * u2, v - q * v2
    return r, u, v


def puzzle2():
    directions, network = get_map()

    # First, run the pathway for each position starting with A, and save the occurrences ending with Z and the moment
    # it starts looping
    pathways = []
    for pos_init in [s for s in network.keys() if s.endswith("A")]:
        print("Processing pathway " + pos_init)
        pos_network = pos_init
        pos_direction = 0
        pathway = []
        while (pos_network, pos_direction) not in pathway:
            pathway.append((pos_network, pos_direction))
            if directions[pos_direction] == 'L':
                pos_network = network[pos_network][0]
            else:
                pos_network = network[pos_network][1]
            pos_direction = (pos_direction + 1) % len(directions)
        stops = [i for (i, (pos_network, pos_direction)) in enumerate(pathway) if pos_network.endswith("Z")]
        start_loop = pathway.index((pos_network, pos_direction))
        length_loop = len(pathway) - start_loop
        pathways.append(Pathway(start_loop, length_loop, stops))

    # Second, concatenate the results
    concat = Pathway(0, 0, [])
    i = 0
    for pathway in pathways:
        print("Start concatenation " + str(i))
        i = i + 1
        concat = concat.concat(pathway)
    print(concat.stops[0])


def get_map():
    network = dict()
    first_line = True
    with open("input_08.txt", "r") as f:
        for ln in f:
            if first_line:
                directions = [x for x in ln if x != '\n']
                first_line = False
                continue
            if ln == '\n':
                continue
            key = ln[0:3]
            left = ln[7:10]
            right = ln[12:15]
            network[key] = (left, right)
    return directions, network


puzzle1()
puzzle2()
