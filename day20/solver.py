from runner_utils import expected_test_result

from itertools import product
from copy import deepcopy

OFFSET_COORDS = [
    (-1, -1), ( 0, -1), ( 1, -1),
    (-1,  0), ( 0,  0), ( 1,  0),
    (-1,  1), ( 0,  1), ( 1,  1),
]


class Registry:
    def __init__(self, enhancement_string):
        self.pixels = {}
        self.enhancement_string = enhancement_string
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0
        self.flicker = int(self.enhancement_string[int(f"{0}" * 9, 2)] == "#")
        self.dispose = False
        self.to_dispose = []

    def register(self, pixel):
        x, y = pixel.position()
        if not self.dispose:
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)
            self.min_x = min(self.min_x, x)
            self.min_y = min(self.min_y, y)
        self.pixels[pixel.position()] = pixel

    @property
    def flicker_value(self):
        return int(self.enhancement_string[int(f"{self.flicker}" * 9, 2)] == "#")

    def get_pixel_at(self, position):
        if not position in self.pixels:
            lit = self.flicker_value
            return Pixel(*position, registry=self, lit=lit)
        return self.pixels[position]

    def generate_bounds(self):
        min_y = self.min_y
        min_x = self.min_x
        max_y = self.max_y
        max_x = self.max_x
        for y in range(min_y - 1, max_y + 2):
            line = []
            for x in range(min_x - 1, max_x + 2):
                pixel = self.get_pixel_at((x, y))
                if pixel.position() not in self.pixels:
                    self.register(pixel)

    def step(self):
        self.generate_bounds()

        needs_change = []
        for pixel in list(self.pixels.values()):
            index = pixel.as_binary
            lit = int(self.enhancement_string[index] == "#")
            if pixel.lit != lit:
                needs_change.append(pixel)

        self.flicker = lit = self.flicker_value
        for pixel in needs_change:
            pixel.lit = int(not pixel.lit)

    def lit_pixels(self):
        return sum([p.lit for p in self.pixels.values()])

    def __repr__(self):
        lines = []
        min_y = self.min_y
        min_x = self.min_x
        max_y = self.max_y
        max_x = self.max_x
        for y in range(min_y - 1, max_y + 2):
            line = []
            for x in range(min_x - 1, max_x + 2):
                pixel = self.get_pixel_at((x, y))
                line.append(pixel.sign())
            lines.append("".join(line))
        return "\n".join(lines)


class Pixel:
    def __init__(self, x, y, registry, lit=0):
        self.x = x
        self.y = y
        self.lit = lit
        self.registry = registry
        self._neighbour_coords = []
        for nx, ny in OFFSET_COORDS:
            self._neighbour_coords.append((self.x + nx, self.y + ny))

    def position(self):
        return (self.x, self.y)

    @property
    def as_binary(self):
        output = ""
        for coord in self._neighbour_coords:
            pixel = self.registry.get_pixel_at(coord)
            output += f"{pixel.lit}"
        return int(output, 2)

    def sign(self):
        return "#" if self.lit else "."


@expected_test_result(35)
def solve1(input):
    lines = [l for l in input.split("\n") if l]
    enhancement_string = lines[0]
    registry = Registry(enhancement_string)
    are_lit = 0
    for y, pixel_line in enumerate(lines[1:]):
        for x, pixel in enumerate(pixel_line):
            lit = int(pixel == "#")
            are_lit += lit
            registry.register(Pixel(x, y, registry, lit))

    for _ in range(2):
        registry.step()

    return registry.lit_pixels()


@expected_test_result(3351)
def solve2(input):
    lines = [l for l in input.split("\n") if l]
    enhancement_string = lines[0]
    registry = Registry(enhancement_string)
    are_lit = 0
    for y, pixel_line in enumerate(lines[1:]):
        for x, pixel in enumerate(pixel_line):
            lit = int(pixel == "#")
            are_lit += lit
            registry.register(Pixel(x, y, registry, lit))

    for i in range(50):
        registry.step()

    return registry.lit_pixels()
