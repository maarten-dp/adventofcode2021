from runner_utils import expected_test_result


def length_prop(length):
    def validate(mapping, value):
        return len(value) == length
    return validate


def deduced_length(key, length):
    def validate(mapping, value):
        return len(set(value) - set(mapping[key])) == length
    return validate


def reverse_deduced_length(key, length):
    def validate(mapping, value):
        return len(set(mapping[key]) - set(value)) == length
    return validate


UNIQUE_PROPS = {
    1: (length_prop(2),),
    4: (length_prop(4),),
    7: (length_prop(3),),
    8: (length_prop(7),),
}

DEDUCED_PROPS = {
    0: (
        length_prop(6),
        reverse_deduced_length(7, 0),
        reverse_deduced_length(4, 1),
    ),
    2: (
        length_prop(5),
        reverse_deduced_length(7, 1),
        reverse_deduced_length(4, 2)
    ),
    3: (
        length_prop(5),
        deduced_length(7, 2),
        deduced_length(4, 2),
    ),
    5: (
        length_prop(5),
        deduced_length(7, 3),
        deduced_length(4, 2),
        reverse_deduced_length(7, 1),
        reverse_deduced_length(4, 1)
    ),
    6: (
        length_prop(6),
        deduced_length(7, 4),
        deduced_length(4, 3),
    ),
    9: (
        length_prop(6),
        reverse_deduced_length(7, 0),
        reverse_deduced_length(4, 0)
    ),
}


@expected_test_result(26)
def solve1(input):
    lines = [l.split(" | ") for l in [l for l in input.split("\n") if l]]
    found = 0

    for numbers, display in lines:
        registry = []
        for number in numbers.split(" "):
            for key, props in UNIQUE_PROPS.items():
                if all([prop(None, number) for prop in props]):
                    registry.append(sorted(number))
        for display_number in display.split(" "):
            if sorted(display_number) in registry:
                found += 1
    return found


def update_mapping(mapping, signals, validator_props):
    for number in signals[:]:
        for key, props in validator_props.items():
            if all([prop(mapping, number) for prop in props]):
                mapping[key] = "".join(sorted(number))
                signals.remove(number)


class Display:
    def __init__(self, signals):
        self.signals = signals
        self.mapping = {}
        self.value_mapping = {}
        self.assess()

    def assess(self):
        update_mapping(self.mapping, self.signals, UNIQUE_PROPS)
        update_mapping(self.mapping, self.signals, DEDUCED_PROPS)
        self.value_mapping = {v: k for k, v in self.mapping.items()}

    def get_value(self, display_number):
        key = "".join(sorted(display_number))
        return self.value_mapping[key]

    def get_display_value(self, display_values):
        display_value = []
        for value in display_values:
            display_value.append(str(self.get_value(value)))
        return int("".join(display_value))


@expected_test_result(61229)
def solve2(input):
    lines = [l.split(" | ") for l in [l for l in input.split("\n") if l]]
    display_sum = 0
    for numbers, display_values in lines:
        display = Display(numbers.split(" "))
        display_sum += display.get_display_value(display_values.split(" "))
    return display_sum
