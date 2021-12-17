import re
from runner_utils import expected_test_result

FIELD_REGEX = "target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)"


class Rect:
    def __init__(self, sx, ex, sy, ey):
        sx, ex, sy, ey = int(sx), int(ex), int(sy), int(ey)

        self.sx = min(sx, ex)
        self.ex = max(sx, ex)
        self.sy = max(sy, ey)
        self.ey = min(sy, ey)

    def contains(self, point):
        within_x = self.sx <= point[0] <= self.ex
        within_y = self.sy >= point[1] >= self.ey
        return within_x and within_y

    def __repr__(self):
        return f"({self.sx},{self.sy}),({self.ex},{self.ey})"


def find_valid_velocities(field):
    initial_x_velocity = 0
    while initial_x_velocity <= field.ex:
        initial_y_velocity = abs(field.ey)
        while initial_y_velocity >= field.ey:
            x = 0
            y = 0
            x_velocity = initial_x_velocity
            y_velocity = initial_y_velocity

            while y >= field.ey:
                x += x_velocity
                y += y_velocity
                if field.contains((x, y)):
                    yield initial_x_velocity, initial_y_velocity
                x_velocity = max(x_velocity - 1, 0)
                y_velocity -= 1
            initial_y_velocity -= 1
        initial_x_velocity += 1


@expected_test_result(45)
def solve1(input):
    field = Rect(*re.match(FIELD_REGEX, input).groups())
    return sum(range(abs(field.ey)))


@expected_test_result(112)
def solve2(input):
    field = Rect(*re.match(FIELD_REGEX, input).groups())
    velocities = set(find_valid_velocities(field))
    return len(velocities)
