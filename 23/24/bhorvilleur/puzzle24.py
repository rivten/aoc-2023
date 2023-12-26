import itertools
import sympy


def pos_cross(hail_1, hail_2):
    (x1, y1, _), (vx1, vy1, _) = hail_1
    (x2, y2, _), (vx2, vy2, _) = hail_2

    # x = x1 + t1.vx1 = x2 + t2.vx2
    # y = y1 + t1.vy1 = y2 + t2.vy2

    if vx1 * vy2 == vx2 * vy1:
        # Parallel move -> not crossing
        return None

    # vy2.x2 - vx2.y2 = vy2x1 + t1.vx1.vy2 - vx2.y1 - t1.vy1.vx2
    t1 = (vy2 * x2 - vx2 * y2 - vy2 * x1 + vx2 * y1) / (vx1 * vy2 - vx2 * vy1)

    # vy1.x1 - vx1.y1 = vy1x2 + t2.vx2.vy1 - vx1.y2 - t2.vy2.vx1
    t2 = (vy1 * x1 - vx1 * y1 - vy1 * x2 + vx1 * y2) / (vx2 * vy1 - vx1 * vy2)

    if t1 < 0 or t2 < 0:
        # Crossing in the past
        return None

    x = x1 + t1 * vx1
    y = y1 + t1 * vy1
    return x, y


def get_hails():
    hails = []
    with open("input_24.txt", "r") as f:
        for ln in f:
            pos = [int(t) for t in ln[:ln.index(" @ ")].split(", ")]
            v = [int(t) for t in ln[ln.index(" @ ") + 3:].replace('\n', '').split(", ")]
            hails.append((tuple(pos), tuple(v)))
    return hails


def puzzle1():
    limit_min = 200000000000000
    limit_max = 400000000000000

    hails = get_hails()
    n = 0
    for hail_1, hail_2 in itertools.product(hails, hails):
        if hail_1 == hail_2:
            continue
        cross = pos_cross(hail_1, hail_2)
        if cross is None:
            continue
        x, y = cross
        if limit_min <= x < limit_max and limit_min <= y < limit_max:
            n += 1
    print(n // 2)


def puzzle2():
    hails = get_hails()

    (x_1, y_1, z_1), (vx_1, vy_1, vz_1) = hails[0]
    (x_2, y_2, z_2), (vx_2, vy_2, vz_2) = hails[1]
    (x_3, y_3, z_3), (vx_3, vy_3, vz_3) = hails[2]

    vx, vy, vz, t1, t2, t3 = sympy.symbols("vx vy vz t1 t2 t3", real=True)
    equations = [sympy.Eq(vx * (t3 - t1) - (x_3 - x_1) - (vx_3 * t3 - vx_1 * t1), 0),
                 sympy.Eq(vy * (t3 - t1) - (y_3 - y_1) - (vy_3 * t3 - vy_1 * t1), 0),
                 sympy.Eq(vz * (t3 - t1) - (z_3 - z_1) - (vz_3 * t3 - vz_1 * t1), 0),
                 sympy.Eq(vx * (t2 - t1) - (x_2 - x_1) - (vx_2 * t2 - vx_1 * t1), 0),
                 sympy.Eq(vy * (t2 - t1) - (y_2 - y_1) - (vy_2 * t2 - vy_1 * t1), 0),
                 sympy.Eq(vz * (t2 - t1) - (z_2 - z_1) - (vz_2 * t2 - vz_1 * t1), 0)]

    res = sympy.solve(equations)

    (vx, vy, vz, t1) = res[0][vx], res[0][vy], res[0][vz], res[0][t1]

    x = x_1 + vx_1*t1 - vx*t1
    y = y_1 + vy_1*t1 - vy*t1
    z = z_1 + vz_1*t1 - vz*t1


    print(str(x+y+z))


puzzle1()
puzzle2()
