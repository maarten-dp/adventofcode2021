import re
from collections import Counter
from itertools import chain

from runner_utils import expected_test_result

RE = "([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)"


def parse_input(input):
    coords = []
    for line in input.split("\n"):
        if not line:
            continue
        coords.append(list(map(int, re.match(RE, line).groups())))
    return coords


def filter_straight_lines(coords):
    straight_lines = []
    for coord in coords:
        x1, y1, x2, y2 = coord
        if x1 == x2 or y1 == y2:
            straight_lines.append(coord)
    return straight_lines


def expand_coords(coords):
    x1, y1, x2, y2 = coords
    x_diff = x2 - x1
    y_diff = y2 - y1

    points = max(abs(x_diff), abs(y_diff)) - 1

    x_interval = int(x_diff / (points + 1))
    y_interval = int(y_diff / (points + 1))

    line = [(x1, y1)]
    for idx, point in enumerate(range(points), start=1):
        x = x1 + (x_interval * idx)
        y = y1 + (y_interval * idx)
        line.append((x, y))
    line.append((x2, y2))
    return line


def find_overlapping_points(lines):
    all_coords = chain(*map(expand_coords, lines))
    return sum([1 for v in Counter(all_coords).values() if v > 1])


@expected_test_result(5)
def solve1(input):
    lines = filter_straight_lines(parse_input(input))
    return find_overlapping_points(lines)


@expected_test_result(12)
def solve2(input):
    lines = parse_input(input)
    return find_overlapping_points(lines)
