from itertools import chain
from runner_utils import expected_test_result


class Tile:
    def __init__(self, value):
        self.value = value
        self.neighbours = []

    def register_neighbour(self, tile):
        self.neighbours.append(tile)
        tile.neighbours.append(self)

    def is_lowest(self):
        return self.value < min([n.value for n in self.neighbours])


def setup_tile_grid(input):
    rows = []
    for line in [l for l in input.split("\n") if l]:
        line_max = len(line)
        row = []
        for idx, value in enumerate(line):
            tile = Tile(int(value))
            if rows:
                tile.register_neighbour(rows[-1][idx])
            if row:
                tile.register_neighbour(row[-1])
            row.append(tile)
        rows.append(row)
    return rows


@expected_test_result(15)
def solve1(input):
    rows = setup_tile_grid(input)
    lowest_points = list([t for t in chain(*rows) if t.is_lowest()])
    return sum([l.value for l in lowest_points]) + len(lowest_points)


@expected_test_result(1134)
def solve2(input):
    rows = setup_tile_grid(input)
    lowest_points = list([t for t in chain(*rows) if t.is_lowest()])

    def map_basin(tile, basin):
        for n in tile.neighbours:
            if n.value == 9:
                continue
            if n not in basin:
                basin.append(n)
                map_basin(n, basin)

    basins = []
    for low_point in lowest_points:
        basin = []
        map_basin(low_point, basin)
        basins.append(basin)

    largest_basins = sorted(basins, key=lambda b: len(b), reverse=True)[:3]

    outcome = 1
    for basin in largest_basins:
        outcome *= len(basin)
    return outcome
