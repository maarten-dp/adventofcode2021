from runner_utils import expected_test_result


def get_right_tile(tile):
    return tile.right


def get_down_tile(tile):
    return tile.down


class Tile:
    def __init__(self):
        self.occupant = None
        self.up = None
        self.down = None
        self.right = None
        self.left = None


    def register_left(self, neighbour):
        self.left = neighbour
        neighbour.right = self

    def register_up(self, neighbour):
        self.up = neighbour
        neighbour.down = self

    def __repr__(self):
        if self.occupant:
            if self.occupant.get_tile == get_right_tile:
                return ">"
            else:
                return "v"
        return '.'


class SeaCucumber:
    def __init__(self, tile, direction):
        self.tile = tile
        if direction == "v":
            self.get_tile = get_down_tile
        else:
            self.get_tile = get_right_tile

    def can_move(self):
        return self.get_tile(self.tile).occupant is None

    def move(self):
        self.tile.occupant = None
        self.tile = self.get_tile(self.tile)
        self.tile.occupant = self


class SeaFloor:
    def __init__(self):
        self.east_facing_cucumbers = []
        self.south_facing_cucumbers = []
        self.rows = []
        self.steps = 0

    @classmethod
    def from_input(cls, input):
        floor = cls()
        for line in [l for l in input.split("\n") if l]:
            row = []
            for y, raw_tile in enumerate(line):
                tile = Tile()
                if raw_tile is not '.':
                    tile.occupant = SeaCucumber(tile, raw_tile)
                    if raw_tile == 'v':
                        floor.south_facing_cucumbers.append(tile.occupant)
                    else:
                        floor.east_facing_cucumbers.append(tile.occupant)
                if floor.rows:
                    tile.register_up(floor.rows[-1][y])
                if row:
                    tile.register_left(row[-1])
                row.append(tile)
            row[0].register_left(tile)
            floor.rows.append(row)
        for y, tile in enumerate(floor.rows[0]):
            tile.register_up(floor.rows[-1][y])
        return floor

    def step(self):
        impasse = True

        to_move = []
        for cucumber in self.east_facing_cucumbers:
            if cucumber.can_move():
                to_move.append(cucumber)
        if to_move:
            impasse = False
        [c.move() for c in to_move]

        to_move = []
        for cucumber in self.south_facing_cucumbers:
            if cucumber.can_move():
                to_move.append(cucumber)
        if to_move:
            impasse = False
        [c.move() for c in to_move]

        self.steps += 1
        return impasse


    def __repr__(self):
        return "\n".join(["".join([str(t) for t in row]) for row in self.rows])


@expected_test_result(58)
def solve1(input):
    floor = SeaFloor.from_input(input)

    at_impasse = floor.step()
    while not at_impasse:
        at_impasse = floor.step()
    return floor.steps


# @expected_test_result(None)
# def solve2(input):
#     pass
