def puzzle1():
    res = -1
    seeds, transformations_per_level = get_almanach(False)
    for seed in seeds:
        value = seed
        for transformations in transformations_per_level:
            value = apply_transformation(transformations, value)
        if res == -1 or res > value:
            res = value
    print(res)


def puzzle2():
    res = -1
    seeds, transformations_per_level = get_almanach(True)
    aggregated_transformations = []
    for transformations in transformations_per_level:
        completeTransformations(transformations)
        aggregated_transformations = concatenate_transformations(aggregated_transformations, transformations)
    for seed_start, length in seeds:
        value = apply_transformation(aggregated_transformations, seed_start)
        if res == -1 or res > value:
            res = value
        for (_, source, _) in aggregated_transformations:
            if seed_start < source < seed_start + length:
                value = apply_transformation(aggregated_transformations, source)
                if res > value:
                    res = value
    print(res)


def apply_transformation(transformations, value):
    for (destination_start, source_start, length) in transformations:
        if source_start <= value < source_start + length:
            return destination_start + value - source_start
    return value


def completeTransformations(transformations):
    sorted_transformations = sorted((s, l) for (_, s, l) in transformations)

    s0 = sorted_transformations[0][0]
    if s0 != 0:
        transformations.append((0, 0, s0))
    for (s1, l1), (s2, _) in zip(sorted_transformations, sorted_transformations[1:]):
        if s2 > s1 + l1:
            transformations.append((s1 + l1, s1 + l1, s2 - s1 - l1))


def concatenate_transformations(transformations1, transformations2):
    if (len(transformations1)) == 0:
        return transformations2

    transformation_limits = {}

    limit_max_1 = max(destination_start + length for (_, destination_start, length) in transformations1)
    limit_max_2 = max(destination_start + length for (_, destination_start, length) in transformations2)

    for (d1, s1, l1) in transformations1:
        value = apply_transformation(transformations2, d1)
        transformation_limits[s1] = value
        for (d2, s2, l2) in transformations2:
            if d1 < s2 < d1 + l1:
                key = s1 + s2 - d1
                transformation_limits[key] = d2
        if d1 < limit_max_2 < d1 + l1:
            key1 = s1 + limit_max_2 - d1
            transformation_limits[key1] = limit_max_2

    transformation_limits[limit_max_1] = apply_transformation(transformations2, limit_max_1)
    for (d2, s2, l2) in transformations2:
        if limit_max_1 < s2:
            transformation_limits[s2] = d2
    if limit_max_1 < limit_max_2:
        transformation_limits[limit_max_1] = limit_max_2

    sorted_transformations = sorted(transformation_limits.items())

    res = []
    for (s1, d1), (s2, d2) in zip(sorted_transformations, sorted_transformations[1:]):
        res.append((d1, s1, s2 - s1))

    return res


def get_almanach(seeds_as_range):
    seeds = []
    transformations_per_level = []
    processing_transformations = []
    seed_line = True
    with open("input_05.txt", "r") as f:
        for ln in f:
            if seed_line:
                seeds = [int(t) for t in ln[len("seeds: "):].split(" ") if t != '\n']
                if seeds_as_range:
                    seeds = [(seeds[2 * i], seeds[2 * i + 1]) for i in range(len(seeds) // 2)]
                seed_line = False
            elif ln == '\n':
                pass
            elif ln.endswith(":\n"):
                if len(processing_transformations) > 0:
                    transformations_per_level.append(processing_transformations)
                    processing_transformations = []
            else:
                transformation = [int(t) for t in ln.split(" ") if t != '\n']
                processing_transformations.append(tuple(transformation))
        if len(processing_transformations) > 0:
            transformations_per_level.append(processing_transformations)
    return seeds, transformations_per_level


puzzle1()
puzzle2()
