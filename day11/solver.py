from runner_utils import expected_test_result

THRESHOLD = 9


class Octopus:
    def __init__(self, energy):
        self.energy = energy
        self.neighbours = set()

    def register_neighbour(self, neighbour):
        self.neighbours.add(neighbour)
        neighbour.neighbours.add(self)

    def increase_energy(self):
        if self.energy <= THRESHOLD:
            self.energy += 1
            if self.energy > THRESHOLD:
                for neighbour in self.neighbours:
                    neighbour.increase_energy()

    def flash(self):
        if self.energy > THRESHOLD:
            self.energy = 0
            return True
        return False

    def __repr__(self):
        return str(self.energy)


class OctopusMap:
    def __init__(self, input):
        self.rows = []
        self.octopi = []
        self.flashes = 0
        for line in input:
            line_max = len(line)
            row = []
            for idx, energy_level in enumerate(line):
                octopus = Octopus(int(energy_level))
                if self.rows:
                    for n in self.rows[-1][max(idx-1, 0):min(idx+2, line_max)]:
                        octopus.register_neighbour(n)
                if row:
                    octopus.register_neighbour(row[-1])
                row.append(octopus)
                self.octopi.append(octopus)
            self.rows.append(row)


    def tick(self):
        for octopus in self.octopi:
            octopus.increase_energy()

        for octopus in self.octopi:
            self.flashes += octopus.flash()


    def __repr__(self):
        return "\n".join([" ".join([str(s) for s in row]) for row in self.rows])


@expected_test_result(1656)
def solve1(input):
    lines = [l for l in input.split("\n") if l]
    omap = OctopusMap(lines)
    for i in range(100):
        omap.tick()
    return omap.flashes


@expected_test_result(195)
def solve2(input):
    lines = [l for l in input.split("\n") if l]
    omap = OctopusMap(lines)

    i = 0
    while True:
        i += 1
        omap.tick()
        if omap.flashes == 100:
            break
        omap.flashes = 0
    return i
