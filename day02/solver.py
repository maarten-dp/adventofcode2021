import operator
from runner_utils import expected_test_result

ACTIONS = {
    "forward": ('x', operator.add),
    "down": ('depth', operator.add),
    "up": ('depth', operator.sub),
}


class YellowSubmarine:
    def __init__(self):
        self.x = 0
        self.depth = 0

    def move(self, action, amount):
        attr, op = ACTIONS[action]
        value = op(getattr(self, attr), amount)
        setattr(self, attr, value)


class BlueSubmarine:
    def __init__(self):
        self.x = 0
        self.depth = 0
        self.aim = 0

    def move(self, action, amount):
        getattr(self, action)(amount)

    def forward(self, amount):
        self.x += amount
        self.depth += amount * self.aim

    def down(self, amount):
        self.aim += amount

    def up(self, amount):
        self.aim -= amount


def perform_actions(sub, input):
    actions = [l for l in input.split("\n") if l]
    for raw_action in actions:
        action, amount = raw_action.split(" ")
        sub.move(action, int(amount))
    return sub.x * sub.depth


@expected_test_result(150)
def solve1(input):
    return perform_actions(YellowSubmarine(), input)


@expected_test_result(900)
def solve2(input):
    return perform_actions(BlueSubmarine(), input)
