from runner_utils import expected_test_result


ENERGY_MAP = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


class Spot:
    def __init__(
        self,
        name,
        destination_for,
        can_rest
    ):
        self.name = name
        self.destination_for = destination_for
        self.can_rest = can_rest
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.current_occupant = None

    def register_right(self, spot):
        self.right = spot
        spot.left = self

    def register_up(self, spot):
        self.up = spot
        spot.down = self

    def moves(self, target_spot, current_cost=None, visited=None):
        if visited is None:
            visited = []
        if current_cost is None:
            current_cost = 1

        moves = []
        for spot in [self.left, self.up, self.right, self.down]:
            if spot is None:
                continue
            if spot in visited:
                continue
            if spot == target_spot:
                return current_cost
            new_visited = visited[:]
            new_visited.append(spot)
            m = spot.moves(target_spot, current_cost + 1, new_visited)
            if m:
                moves.append(m)
        if moves:
            return min(moves)

    def copy(self):
        spot_copy = Spot(self.name, self.destination_for, self.can_rest)
        if self.right:
            spot_copy.register_right(self.right.copy())
        if self.down:
            self.down.copy().register_up(spot_copy)
        if self.current_occupant:
            spot_copy.current_occupant = self.current_occupant.copy(spot_copy)
        return spot_copy

    def get_amphipods(self):
        if self.current_occupant:
            yield self.current_occupant
        if self.right:
            yield from self.right.get_amphipods()
        if self.down:
            yield from self.down.get_amphipods()

    def get_rooms(self):
        if self.right:
            yield self.right
            yield from self.right.get_rooms()
        if self.down:
            yield self.down
            yield from self.down.get_rooms()

    def __repr__(self):
        return self.name


class Amphipod:
    def __init__(self, name, atype, spot):
        self.name = name
        self.atype = atype
        self.spot = spot

    def get_valid_moves(self):
        def get_available_moves(spot, visited):
            moves = []
            for direction in [spot.left, spot.up, spot.right, spot.down]:
                if direction in visited:
                    continue
                if direction is None:
                    continue
                if direction.current_occupant is not None:
                    continue
                new_visited = visited[:]
                new_visited.append(direction)
                moves.extend(get_available_moves(direction, new_visited))
                moves.append(direction)
            return moves

        def key(item):
            return self.spot.moves(item) * ENERGY_MAP[self.atype]

        available_moves = sorted(get_available_moves(self.spot, []), key=key)
        spots = []
        for spot in available_moves:
            if spot.destination_for == self.atype:
                if spot.down:
                    occupant = spot.down.current_occupant
                    if occupant and occupant.locked_in():
                        return [spot]
                else:
                    return [spot]
            
            if not spot.destination_for and spot.can_rest:
                if not self.spot.can_rest:
                    spots.append(spot)
        return spots

    def locked_in(self):
        if self.spot.destination_for == self.atype:
            if self.spot.down is None:
                return True
            else:
                if self.spot.down.current_occupant:
                    occupant = self.spot.down.current_occupant
                    if self.spot.down.destination_for == occupant.atype:
                        return True
        return False


    def move_to(self, spot):
        cost = self.spot.moves(spot)
        self.spot.current_occupant = None
        spot.current_occupant = self
        self.spot = spot
        return cost

    def copy(self, spot):
        return Amphipod(self.name, self.atype, spot)

    def __repr__(self):
        return self.atype

    def __str__(self):
        return self.__repr__()


class Enclosure:
    def __init__(self, top_left):
        self.top_left = top_left

    def copy(self):
        return Enclosure(self.top_left.copy())

    @property
    def amphipods(self):
        def key(item):
            return ENERGY_MAP[item.atype]
        return sorted(self.top_left.get_amphipods(), key=key)

    def get_amphipod(self, name):
        for amphipod in self.amphipods:
            if amphipod.name == name:
                return amphipod

    def get_room(self, name):
        if self.top_left.name == name:
            return self.top_left
        for room in self.top_left.get_rooms():
            if room.name == name:
                return room

    def locked_in(self):
        return all([a.locked_in() for a in self.amphipods])


def build_part1_enclosure(input):
    # hallway
    left_2 = Spot("left_2" ,None, True)
    left_1 = Spot("left_1" ,None, True)
    exit_a = Spot("exit_a" ,None, False)
    ab = Spot("ab" ,None, True)
    exit_b = Spot("exit_b" ,None, False)
    bc = Spot("bc" ,None, True)
    exit_c = Spot("exit_c" ,None, False)
    cd = Spot("cd" ,None, True)
    exit_d = Spot("exit_d" ,None, False)
    right_1 = Spot("right_1" ,None, True)
    right_2 = Spot("right_2" ,None, True)
    spots = (left_2, left_1, exit_a, ab, exit_b, bc, exit_c, cd, exit_d, right_1, right_2)
    for spot1, spot2 in zip(spots, spots[1:]):
        spot1.register_right(spot2)

    # rooms
    room_a1 = Spot("room_a1" ,"A", False)
    room_a2 = Spot("room_a2" ,"A", False)
    room_a1.register_up(room_a2)
    room_a2.register_up(exit_a)

    room_b1 = Spot("room_b1" ,"B", False)
    room_b2 = Spot("room_b2" ,"B", False)
    room_b1.register_up(room_b2)
    room_b2.register_up(exit_b)

    room_c1 = Spot("room_c1" ,"C", False)
    room_c2 = Spot("room_c2" ,"C", False)
    room_c1.register_up(room_c2)
    room_c2.register_up(exit_c)

    room_d1 = Spot("room_d1" ,"D", False)
    room_d2 = Spot("room_d2" ,"D", False)
    room_d1.register_up(room_d2)
    room_d2.register_up(exit_d)

    rooms = {
        "left_2": left_2,
        **{r.name: r for r in left_2.get_rooms()}
    }

    lines = [l for l in input.split("\n") if l]
    a,b,c,d = lines[2].strip("#").split("#")
    rooms["room_a2"].current_occupant = Amphipod(f"{a}1", a, rooms["room_a2"])
    rooms["room_b2"].current_occupant = Amphipod(f"{b}2", b, rooms["room_b2"])
    rooms["room_c2"].current_occupant = Amphipod(f"{c}3", c, rooms["room_c2"])
    rooms["room_d2"].current_occupant = Amphipod(f"{d}4", d, rooms["room_d2"])
    a,b,c,d = lines[3].strip()[1:-1].split("#")
    rooms["room_a1"].current_occupant = Amphipod(f"{a}5", a, rooms["room_a1"])
    rooms["room_b1"].current_occupant = Amphipod(f"{b}6", b, rooms["room_b1"])
    rooms["room_c1"].current_occupant = Amphipod(f"{c}7", c, rooms["room_c1"])
    rooms["room_d1"].current_occupant = Amphipod(f"{d}8", d, rooms["room_d1"])

    return Enclosure(rooms["left_2"])


def build_part2_enclosure(input):
    # hallway
    left_2 = Spot("left_2" ,None, True)
    left_1 = Spot("left_1" ,None, True)
    exit_a = Spot("exit_a" ,None, False)
    ab = Spot("ab" ,None, True)
    exit_b = Spot("exit_b" ,None, False)
    bc = Spot("bc" ,None, True)
    exit_c = Spot("exit_c" ,None, False)
    cd = Spot("cd" ,None, True)
    exit_d = Spot("exit_d" ,None, False)
    right_1 = Spot("right_1" ,None, True)
    right_2 = Spot("right_2" ,None, True)
    spots = (left_2, left_1, exit_a, ab, exit_b, bc, exit_c, cd, exit_d, right_1, right_2)
    for spot1, spot2 in zip(spots, spots[1:]):
        spot1.register_right(spot2)

    # rooms
    room_a1 = Spot("room_a1" ,"A", False)
    room_a2 = Spot("room_a2" ,"A", False)
    room_a3 = Spot("room_a3" ,"A", False)
    room_a4 = Spot("room_a4" ,"A", False)
    room_a1.register_up(room_a2)
    room_a2.register_up(room_a3)
    room_a3.register_up(room_a4)
    room_a4.register_up(exit_a)

    room_b1 = Spot("room_b1" ,"B", False)
    room_b2 = Spot("room_b2" ,"B", False)
    room_b3 = Spot("room_b3" ,"B", False)
    room_b4 = Spot("room_b4" ,"B", False)
    room_b1.register_up(room_b2)
    room_b2.register_up(room_b3)
    room_b3.register_up(room_b4)
    room_b4.register_up(exit_b)

    room_c1 = Spot("room_c1" ,"C", False)
    room_c2 = Spot("room_c2" ,"C", False)
    room_c3 = Spot("room_c3" ,"C", False)
    room_c4 = Spot("room_c4" ,"C", False)
    room_c1.register_up(room_c2)
    room_c2.register_up(room_c3)
    room_c3.register_up(room_c4)
    room_c4.register_up(exit_c)

    room_d1 = Spot("room_d1" ,"D", False)
    room_d2 = Spot("room_d2" ,"D", False)
    room_d3 = Spot("room_d3" ,"D", False)
    room_d4 = Spot("room_d4" ,"D", False)
    room_d1.register_up(room_d2)
    room_d2.register_up(room_d3)
    room_d3.register_up(room_d4)
    room_d4.register_up(exit_d)

    rooms = {
        "left_2": left_2,
        **{r.name: r for r in left_2.get_rooms()}
    }

    lines = [l for l in input.split("\n") if l]
    lines.insert(3, "#D#B#A#C#")
    lines.insert(3, "#D#C#B#A#")

    a,b,c,d = lines[2].strip("#").split("#")
    rooms["room_a4"].current_occupant = Amphipod(f"{a}1", a, rooms["room_a4"])
    rooms["room_b4"].current_occupant = Amphipod(f"{b}2", b, rooms["room_b4"])
    rooms["room_c4"].current_occupant = Amphipod(f"{c}3", c, rooms["room_c4"])
    rooms["room_d4"].current_occupant = Amphipod(f"{d}4", d, rooms["room_d4"])
    a,b,c,d = lines[3].strip()[1:-1].split("#")
    rooms["room_a3"].current_occupant = Amphipod(f"{a}5", a, rooms["room_a3"])
    rooms["room_b3"].current_occupant = Amphipod(f"{b}6", b, rooms["room_b3"])
    rooms["room_c3"].current_occupant = Amphipod(f"{c}7", c, rooms["room_c3"])
    rooms["room_d3"].current_occupant = Amphipod(f"{d}8", d, rooms["room_d3"])
    a,b,c,d = lines[4].strip()[1:-1].split("#")
    rooms["room_a2"].current_occupant = Amphipod(f"{a}9", a, rooms["room_a2"])
    rooms["room_b2"].current_occupant = Amphipod(f"{b}10", b, rooms["room_b2"])
    rooms["room_c2"].current_occupant = Amphipod(f"{c}11", c, rooms["room_c2"])
    rooms["room_d2"].current_occupant = Amphipod(f"{d}12", d, rooms["room_d2"])
    a,b,c,d = lines[5].strip()[1:-1].split("#")
    rooms["room_a1"].current_occupant = Amphipod(f"{a}13", a, rooms["room_a1"])
    rooms["room_b1"].current_occupant = Amphipod(f"{b}14", b, rooms["room_b1"])
    rooms["room_c1"].current_occupant = Amphipod(f"{c}15", c, rooms["room_c1"])
    rooms["room_d1"].current_occupant = Amphipod(f"{d}16", d, rooms["room_d1"])

    return Enclosure(rooms["left_2"])


def find_cheapest_bfs(enclosure, current_cost, current_cheapest):
    costs = []
    for amphipod in enclosure.amphipods:
        if amphipod.locked_in():
            continue

        for spot in amphipod.get_valid_moves():
            enclosure_copy = enclosure.copy()
            amphipod_copy = enclosure_copy.get_amphipod(amphipod.name)
            spot_copy = enclosure_copy.get_room(spot.name)
            moves = amphipod_copy.move_to(spot_copy)
            cost = ENERGY_MAP[amphipod_copy.atype] * moves

            if current_cheapest:
                if current_cost + cost >= current_cheapest[0]:
                    continue

            if enclosure_copy.locked_in():
                if current_cheapest:
                    cheapest = min(current_cheapest[0], current_cost + cost)
                    if cheapest != current_cheapest[0]:
                        print(cheapest)
                    current_cheapest[0] = cheapest
                else:
                    current_cheapest.append(current_cost + cost)
                continue

            costs.append((current_cost + cost, enclosure_copy))

    for cost, enclosure in costs:
        find_cheapest_bfs(enclosure, cost, current_cheapest)


@expected_test_result(None)
def solve1(input):
    enclosure = build_part1_enclosure(input)
    cheapest = []
    find_cheapest_bfs(enclosure, 0, cheapest)
    return cheapest[0]


@expected_test_result(None)
def solve2(input):
    enclosure = build_part2_enclosure(input)
    cheapest = []
    find_cheapest_bfs(enclosure, 0, cheapest)
    return cheapest[0]
