from runner_utils import expected_test_result


class Cube:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.is_on = False


class Registry:
    def __init__(self):
        self.registry = {}

    def get_cube_at(self, position):
        if position not in self.registry:
            self.registry[position] = Cube(*position)
        return self.registry[position]


def parse_input(input):
    actions = []
    for line in input.split("\n"):
        if not line:
            continue
        action, ranges = line.split(" ")
        action = action == "on"
        x_range, y_range, z_range = ranges.split(",")
        x_range = x_range[2:].split("..")
        y_range = y_range[2:].split("..")
        z_range = z_range[2:].split("..")
        actions.append((action, x_range, y_range, z_range))
    return actions


def do_thing():
    def get_start_end(range):
        start, end = range
        start = max(int(start), -50)
        end = min(int(end), 50) + 1
        return start, end

    registry = Registry()
    for idx, (action, x_range, y_range, z_range) in enumerate(parse_input()):
        print(idx)
        for x in range(*get_start_end(x_range)):
            for y in range(*get_start_end(y_range)):
                for z in range(*get_start_end(z_range)):
                    cube = registry.get_cube_at((x, y, z))
                    cube.is_on = action
    print(sum([c.is_on for c in registry.registry.values()]))


class CubeRange:
    def __init__(self, xs, xe, ys, ye, zs, ze):
        self.xs, self.xe = xs, xe
        self.ys, self.ye = ys, ye
        self.zs, self.ze = zs, ze

    def copy(self):
        return CubeRange(self.xs, self.xe, self.ys, self.ye, self.zs, self.ze)

    def subtract_range(self, cube_range):
        cubes = []
        if not self.has_overlap(cube_range):
            return [self]

        if self.xs < cube_range.xs:
            cube = self.copy()
            cube.xe = cube_range.xs - 1
            cubes.append(cube)
        if cube_range.xe < self.xe:
            cube = self.copy()
            cube.xs = cube_range.xe + 1
            cubes.append(cube)

        if self.ys < cube_range.ys:
            cube = self.copy()
            cube.xs = max(cube_range.xs, cube.xs)
            cube.xe = min(cube_range.xe, cube.xe)
            cube.ye = cube_range.ys - 1
            cubes.append(cube)
        if cube_range.ye < self.ye:
            cube = self.copy()
            cube.xs = max(cube_range.xs, cube.xs)
            cube.xe = min(cube_range.xe, cube.xe)
            cube.ys = cube_range.ye + 1
            cubes.append(cube)

        if self.zs < cube_range.zs:
            cube = self.copy()
            cube.xs = max(cube_range.xs, cube.xs)
            cube.xe = min(cube_range.xe, cube.xe)
            cube.ys = max(cube_range.ys, cube.ys)
            cube.ye = min(cube_range.ye, cube.ye)
            cube.ze = cube_range.zs - 1
            cubes.append(cube)
        if cube_range.ze < self.ze:
            cube = self.copy()
            cube.xs = max(cube_range.xs, cube.xs)
            cube.xe = min(cube_range.xe, cube.xe)
            cube.ys = max(cube_range.ys, cube.ys)
            cube.ye = min(cube_range.ye, cube.ye)
            cube.zs = cube_range.ze + 1
            cubes.append(cube)

        return cubes

    @property
    def active_cubes(self):
        x = abs(self.xe - self.xs) + 1
        y = abs(self.ye - self.ys) + 1
        z = abs(self.ze - self.zs) + 1
        return x * y * z

    def has_overlap(self, cube_range):
        if not self.has_x_overlap(cube_range):
            return False
        if not self.has_y_overlap(cube_range):
            return False
        if not self.has_z_overlap(cube_range):
            return False
        return True

    def has_x_overlap(self, cube_range):
        start_overlap = cube_range.xs <= self.xe
        end_overlap = cube_range.xe >= self.xs
        return start_overlap and end_overlap

    def has_y_overlap(self, cube_range):
        start_overlap = cube_range.ys <= self.ye
        end_overlap = cube_range.ye >= self.ys
        return start_overlap and end_overlap

    def has_z_overlap(self, cube_range):
        start_overlap = cube_range.zs <= self.ze
        end_overlap = cube_range.ze >= self.zs
        return start_overlap and end_overlap

    def __repr__(self):
        return f"CubeRange({self.xs},{self.xe},{self.ys},{self.ye},{self.zs},{self.ze})"


@expected_test_result(590784)
def solve1(input):
    def get_start_end(axis_range):
        start, end = axis_range
        start = int(start)
        end = int(end)
        return start, end

    ranges = []
    for idx, (action, x_range, y_range, z_range) in enumerate(parse_input(input)):
        new_ranges = []
        cube_range = CubeRange(
            *get_start_end(x_range),
            *get_start_end(y_range),
            *get_start_end(z_range),
        )

        if not ranges:
            ranges.append(cube_range)
            continue

        new_ranges = []
        for existing_range in ranges:
            new_ranges.extend(existing_range.subtract_range(cube_range))

        if action:
            new_ranges.append(cube_range)
        ranges = new_ranges
    return sum([r.active_cubes for r in ranges])


@expected_test_result(2758514936282235)
def solve2(input):
    def get_start_end(axis_range):
        start, end = axis_range
        start = min(int(start), int(end))
        end = max(int(start), int(end))
        return start, end

    ranges = []
    for idx, (action, x_range, y_range, z_range) in enumerate(parse_input(input)):
        new_ranges = []
        cube_range = CubeRange(
            *get_start_end(x_range),
            *get_start_end(y_range),
            *get_start_end(z_range),
        )
        if not ranges:
            ranges.append(cube_range)
            continue

        new_ranges = []
        for existing_range in ranges:
            new_ranges.extend(existing_range.subtract_range(cube_range))

        if action:
            new_ranges.append(cube_range)
        ranges = new_ranges
    return sum([r.active_cubes for r in ranges])
