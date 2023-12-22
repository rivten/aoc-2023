import math
from abc import ABC
from queue import Queue

PULSE_HIGH = True
PULSE_LOW = False


class Module(ABC):

    def __init__(self, name):
        self.followers = list()
        self.name = name
        # Will serve to detect that the module has received a low pulse in puzzle 2
        self.buzzer = False

    def __repr__(self) -> str:
        return self.name

    def add_follower(self, follower):
        self.followers.append(follower)

    def process_low_pulse(self, sender):
        self.buzzer = True
        return None

    def process_high_pulse(self, sender, i):
        return None


class FlipFlop(Module):

    def __init__(self, name):
        super().__init__(name)
        self.state_on = False

    def process_low_pulse(self, sender):
        super().process_low_pulse(sender)
        self.state_on = not self.state_on
        return PULSE_HIGH if self.state_on else PULSE_LOW

    def process_high_pulse(self, sender, count):
        if self.name in ["vd", "ns", "bh", "dl"]:
            print(" > " + self.name + " : " + str(count))
        return None


class Conjunction(Module):

    def __init__(self, name):
        super().__init__(name)
        self.last_signals = {}
        self.loops = {}

    def add_previous(self, module):
        self.last_signals[module] = PULSE_LOW
        self.loops[module] = [None]

    def process_low_pulse(self, sender):
        super().process_low_pulse(sender)
        self.last_signals[sender] = PULSE_LOW
        return PULSE_HIGH

    def process_high_pulse(self, sender, count):
        self.last_signals[sender] = PULSE_HIGH
        return PULSE_LOW if len([s for (s, v) in self.last_signals.items() if v == PULSE_LOW]) == 0 else PULSE_HIGH


def push_button(broadcasted_modules, i=0):
    scheduler = Queue()

    low_pulses, high_pulses = 1, 0

    for module in broadcasted_modules:
        scheduler.put(("broadcaster", module, PULSE_LOW))
    while not scheduler.empty():
        (sender, module, pulse) = scheduler.get()

        if pulse == PULSE_LOW:
            low_pulses += 1
            answer = module.process_low_pulse(sender)
        else:
            high_pulses += 1
            answer = module.process_high_pulse(sender, i)
        if answer is None:
            continue
        for follower in module.followers:
            scheduler.put((module, follower, answer))

    return low_pulses, high_pulses


def build_modules(serialized_graph: dict):
    modules = dict()
    broadcasted_modules = []
    for key in serialized_graph.keys():
        if key != "broadcaster":
            type, name = key
            if type == '%':
                modules[name] = FlipFlop(name)
            else:
                modules[name] = Conjunction(name)

    for (key, value) in serialized_graph.items():
        for name in value:
            if name not in modules:
                modules[name] = Module(name)
        followers = [modules[k] for k in value]
        if key == "broadcaster":
            broadcasted_modules = followers
        else:
            type, name = key
            module = modules[name]
            for follower in followers:
                module.add_follower(follower)
                if isinstance(follower, Conjunction):
                    follower.add_previous(module)

    return broadcasted_modules, modules


def get_serialized_graph():
    serialized_graph = {}
    with open("input_20.txt", "r") as f:
        for ln in f:
            key = ln[:ln.index(" -> ")]
            if key != "broadcaster":
                key = key[0], key[1:]
            values = ln[ln.index(" -> ") + 4:].replace("\n", "").split(", ")
            serialized_graph[key] = values
    return serialized_graph


def puzzle1():
    serialized_graph = get_serialized_graph()
    broadcasted_modules, _ = build_modules(serialized_graph)
    low_pulses, high_pulses = 0, 0
    for i in range(1000):
        tmp_low_pulses, tmp_high_pulses = push_button(broadcasted_modules)
        low_pulses += tmp_low_pulses
        high_pulses += tmp_high_pulses

    print(low_pulses)


def lcm(cycles):
    values = [val for (i_, val) in cycles.items()]
    res = values[0]
    for i in values[1:]:
        res = res * i // math.gcd(res, i)
    return res


def puzzle2():
    serialized_graph = get_serialized_graph()
    broadcasted_modules, modules = build_modules(serialized_graph)
    zh_module = modules["zh"]
    previous_modules_cycles = {module: None for module in modules.values() if zh_module in module.followers}
    count = 0
    remaining_cycles = len(previous_modules_cycles)
    while remaining_cycles > 0:
        push_button(broadcasted_modules, count)
        count += 1
        for module in previous_modules_cycles.keys():
            if module.buzzer and previous_modules_cycles[module] is None:
                previous_modules_cycles[module] = count
                module.buzzer = False
                remaining_cycles -= 1

    print(lcm(previous_modules_cycles))


puzzle1()
puzzle2()
