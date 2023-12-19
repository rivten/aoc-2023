from copy import deepcopy
from typing import Dict

import numpy

CATEGORIES = {'x': 0, 'm': 1, 'a': 2, 's': 3}


class Rule:

    def __init__(self, cat, rule_type, comp):
        self.cat = cat
        self.rule_type = rule_type
        self.comp = comp

    # Returns True if the rule is respected for the given part, False otherwise
    def apply(self, part):
        val = part[CATEGORIES[self.cat]]
        if self.rule_type == '<':
            return val < self.comp
        else:
            return val > self.comp

    # Takes a range of parts and split it in two ranges : the first oneis the range of parts that don't respect
    # the rule, the second one is the range of parts that respect the rule.
    def apply_range(self, part_range):
        range_cat = part_range[CATEGORIES[self.cat]]
        if self.rule_type == '<' and self.comp <= range_cat[0]:
            return part_range, None
        if self.rule_type == '<' and self.comp >= range_cat[1]:
            return None, part_range
        if self.rule_type == '>' and self.comp < range_cat[0]:
            return None, part_range
        if self.rule_type == '>' and self.comp >= range_cat[1] - 1:
            return part_range, None

        range_false, range_true = deepcopy(part_range), deepcopy(part_range)
        if self.rule_type == '<':
            range_true[CATEGORIES[self.cat]][1] = self.comp
            range_false[CATEGORIES[self.cat]][0] = self.comp
        else:
            range_false[CATEGORIES[self.cat]][1] = self.comp + 1
            range_true[CATEGORIES[self.cat]][0] = self.comp + 1
        return range_false, range_true

    def __eq__(self, o: object) -> bool:
        return (self.cat, self.rule_type, self.comp) == o

    def __ne__(self, o: object) -> bool:
        return (self.cat, self.rule_type, self.comp) != o

    def __str__(self) -> str:
        return str((self.cat, self.rule_type, self.comp))

    def __repr__(self) -> str:
        return repr((self.cat, self.rule_type, self.comp))

    def __hash__(self) -> int:
        return hash((self.cat, self.rule_type, self.comp))


class Workflow:

    def __init__(self, rules: Dict[Rule, str], default_val: str):
        self.rules = rules
        self.default_val = default_val

    # Apply the workflow to a part and returns the subsequent label
    def apply(self, part):
        for rule, label in self.rules.items():
            if rule.apply(part):
                return label
        return self.default_val

    # Apply the workflow to a range of parts, and returns the partition of the part range by the subsequent labels.
    def apply_range(self, part_range):
        res = dict()
        for rule, label in self.rules.items():
            range_false, range_true = rule.apply_range(part_range)
            if range_true is not None:
                if label not in res:
                    res[label] = []
                res[label].append(range_true)
            part_range = range_false
            if part_range is None:
                break

        if part_range is not None:
            if self.default_val not in res:
                res[self.default_val] = []
            res[self.default_val].append(part_range)
        return res


def puzzle1():
    workflows, parts = parse_file()

    res = 0
    for part in parts:
        workflow = workflows["in"]
        c = True
        while c:
            str = workflow.apply(part)
            if str == 'A':
                res += sum(part)
                c = False
            elif str == 'R':
                c = False
            else:
                workflow = workflows[str]

    print(res)


# Take a series of part ranges, and compute its volume (product of size for the 4 components)
def get_size(part_range_series):
    return sum([numpy.prod([t[1] - t[0] for t in p], dtype='int64') for p in part_range_series])


# Take two series of part ranges series and complete the first one with the ranges of the second one
def append_part_range_series(part_ranges_series, part_ranges_series_2):
    for label, part_ranges in part_ranges_series_2.items():
        if label not in part_ranges_series:
            part_ranges_series[label] = []
        part_ranges_series[label].extend(part_ranges)


def puzzle2():
    workflows, _ = parse_file()
    part_ranges_series = {"in": [[[1, 4001], [1, 4001], [1, 4001], [1, 4001]]]}

    res_accepted, res_refused = 0, 0
    while len(part_ranges_series) > 0: # While some values are not accepted nor refused
        new_part_ranges = dict()
        for label, part_ranges in part_ranges_series.items():
            if label == "A":
                res_accepted += get_size(part_ranges)
                continue
            if label == 'R':
                res_refused += get_size(part_ranges)
                continue

            for part_range in part_ranges:
                append_part_range_series(new_part_ranges, workflows[label].apply_range(part_range))
        part_ranges_series = new_part_ranges
    print(res_accepted)
    assert (res_accepted + res_refused == 4000 * 4000 * 4000 * 4000)


def parse_file():
    workflows = {}
    parts = []
    with open("input_19.txt", "r") as f:
        process_parts = False
        for ln in f:
            if ln == '\n':
                process_parts = True
            elif process_parts:
                parts.append([int(s[2:]) for s in ln[1:ln.index("}")].split(',')])
            else:
                key = ln[:ln.index("{")]
                str_rules = ln[ln.index("{") + 1:ln.index("}")].split(",")
                rules = {}
                for str_rule in str_rules[:-1]:
                    cat = str_rule[0]
                    sign = str_rule[1]
                    comp = int(str_rule[2:str_rule.index(":")])
                    val = str_rule[str_rule.index(":") + 1:]
                    rules[Rule(cat, sign, comp)] = val
                default_val = str_rules[-1]
                workflows[key] = Workflow(rules, default_val)
    return workflows, parts


puzzle1()
puzzle2()
