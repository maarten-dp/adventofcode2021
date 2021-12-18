from runner_utils import expected_test_result
import math


def pair_from_value(value):
    left = math.floor(value / 2)
    right = math.ceil(value / 2)
    return Pair(left, right)


class Pair:
    def __init__(self, left_value, right_value):
        if isinstance(left_value, list):
            left_value = Pair(*left_value)
        if isinstance(right_value, list):
            right_value = Pair(*right_value)

        self.left_value = left_value
        self.right_value = right_value
        self.parent = None
        self._register_parents()


    def _register_parents(self):
        pair = [self.left_value, self.right_value]
        for item in pair:
            if isinstance(item, Pair):
                if item.parent is None:
                    item.parent = self

    def resolve(self):
        if isinstance(self.left_value, int):
            left_value = self.left_value
        else:
            left_value = self.left_value.resolve()

        if isinstance(self.right_value, int):
            right_value = self.right_value
        else:
            right_value = self.right_value.resolve()
        return (3 * left_value) + (2 * right_value)

    def add(self):
        def explode():
            explosive = self.find_first_explosive()
            while explosive:
                explosive.explode()
                explosive = self.find_first_explosive()
        explode()
        splitting = self.find_first_splitter()
        while splitting:
            splitting.split()
            explode()
            splitting = self.find_first_splitter()

    def find_first_explosive(self):
        if self.depth > 3:
            return self
        explosive = None
        if not isinstance(self.left_value, int):
            explosive = self.left_value.find_first_explosive()
        if not explosive and not isinstance(self.right_value, int):
            explosive = self.right_value.find_first_explosive()
        return explosive

    def find_first_splitter(self):
        splitting = None
        if isinstance(self.left_value, int):
            if self.left_value >= 10:
                return self
        else:
            splitting = self.left_value.find_first_splitter()

        if not splitting:
            if isinstance(self.right_value, int):
                if self.right_value >= 10:
                    return self
            else:
                splitting = self.right_value.find_first_splitter()
        return splitting

    def split(self):
        pair = None
        if isinstance(self.left_value, int) and self.left_value >= 10:
            pair = pair_from_value(self.left_value)
            pair.parent = self
            self.left_value = pair
        elif isinstance(self.right_value, int) and self.right_value >= 10:
            pair = pair_from_value(self.right_value)
            pair.parent = self
            self.right_value = pair

    def explode(self):
        self.explode_to_closest(self.left_value, "left_value")
        self.explode_to_closest(self.right_value, "right_value")

        if self.parent.left_value is self:
            self.parent.left_value = 0
        else:
            self.parent.right_value = 0

    def explode_to_closest(self, value, direction):
        if not self.parent:
            return

        opposite_direction = "right_value"
        if direction == "right_value":
            opposite_direction = "left_value"

        if getattr(self.parent, direction) is self:
            self.parent.explode_to_closest(value, direction)
        else:
            if isinstance(getattr(self.parent, direction), int):
                leaf_value = getattr(self.parent, direction)
                setattr(self.parent, direction, leaf_value + value)
            else:
                parent_value = getattr(self.parent, direction)
                pair = self.parent
                while pair:
                    if isinstance(parent_value, int):
                        leaf_value = getattr(pair, opposite_direction)
                        setattr(pair, opposite_direction, leaf_value + value)
                        break
                    pair = parent_value
                    parent_value = getattr(parent_value, opposite_direction)

    @property
    def depth(self):
        parent = self.parent
        depth = 0
        while parent is not None:
            depth += 1
            parent = parent.parent
        return depth

    def __repr__(self):
        return f"[{self.left_value},{self.right_value}]"



@expected_test_result(4140)
def solve1(input):
    pairs = [p for p in input.split("\n") if p]
    left_pair = Pair(*eval(pairs.pop(0)))
    while pairs:
        right_pair = Pair(*eval(pairs.pop(0)))
        left_pair = Pair(left_pair, right_pair)
        left_pair.add()
    return left_pair.resolve()


@expected_test_result(3993)
def solve2(input):
    pairs = [p for p in input.split("\n") if p]
    highest_magnitude = 0
    unresolved = set()

    def get_magnitude(p1, p2):
        p = Pair(Pair(*eval(p1)), Pair(*eval(p2)))
        p.add()
        return p.resolve()

    for p1 in pairs:
        for p2 in pairs:
            if p1 == p2:
                continue
            highest_magnitude = max(highest_magnitude, get_magnitude(p1, p2))
            highest_magnitude = max(highest_magnitude, get_magnitude(p2, p1))
    return highest_magnitude
