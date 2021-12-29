from runner_utils import expected_test_result
from collections import defaultdict


class ALU:
    def __init__(self, input):
        self.reg = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        self.actions = {
            "inp": self.inp,
            "add": self.add,
            "mul": self.mul,
            "div": self.div,
            "mod": self.mod,
            "eql": self.eql,
        }
        self.input = input

    def parse_value(self, value):
        if value in "wxyz":
            return self.reg[value]
        return int(value)

    def inp(self, reg):
        self.reg[reg] = self.input.pop(0)

    def add(self, reg1, value):
        self.reg[reg1] += self.parse_value(value)

    def mul(self, reg1, value):
        self.reg[reg1] *= self.parse_value(value)

    def div(self, reg1, value):
        self.reg[reg1] //= self.parse_value(value)

    def mod(self, reg1, value):
        self.reg[reg1] %= self.parse_value(value)

    def eql(self, reg1, value):
        self.reg[reg1] = int(self.reg[reg1] == self.parse_value(value))

    def read_instruction(self, operation):
        action, registries = operation.split(" ", 1)
        self.actions[action](*registries.split(" "))


def get_serial_number(input, highest):
    sections = []
    section = []
    for operation in reversed([l for l in input.split("\n") if l]):
        section.insert(0, operation)
        if operation.startswith("inp"):
            sections.insert(0, section)
            section = []

    return find_z(list(reversed(sections)), [0], highest)


def find_z(sections, valid_z, highest=True):
    section = sections[0]

    wrange = range(1, 10)
    if highest:
        wrange = reversed(wrange)

    for w in wrange:
        zs = find_candidates(section, w, valid_z)
        if not zs:
            continue
        if not sections[1:]:
            return f"{w}"
        val = find_z(sections[1:], zs, highest)
        if val:
            return f"{val}{w}"

RANGE = list(range(-10000, 10000))
CONFS_PER_SECTIONS = {}


def find_candidates(section, w, valid_conf):
    key = "".join(section) + str(w)
    if key in CONFS_PER_SECTIONS:
        result = CONFS_PER_SECTIONS[key]
    else:
        result = find_z_for_section(section, w)
        CONFS_PER_SECTIONS[key] = result

    valid_configurations = []
    for valid in valid_conf:
        valid_configurations.extend(result.get(valid, []))
    return valid_configurations


def find_z_for_section(section, w):
    results = defaultdict(list)
    for z in RANGE:
        alu = ALU([w])
        starting_conf = {
            "x": 0,
            "y": 0,
            "z": z,
        }
        alu.reg.update(starting_conf)
        for operation in section:
            alu.read_instruction(operation)
        results[alu.reg["z"]].append(z)
    return results


@expected_test_result(None)
def solve1(input):
    print(get_serial_number(input, True))


@expected_test_result(None)
def solve2(input):
    print(get_serial_number(input, False))
