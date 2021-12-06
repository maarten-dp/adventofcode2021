from runner_utils import expected_test_result


class LanternFish:
    def __init__(self, registry, clock=9):
        self.intenal_clock = clock
        self.registry = registry
        self.registry.append(self)

    def tick(self):
        self.intenal_clock -= 1

        if self.intenal_clock < 0:
            LanternFish(registry=self.registry)
            self.intenal_clock = 6


# Naive approach ;)
@expected_test_result(5934)
def solve1(input):
    registry = []
    [LanternFish(registry, int(c)) for c in input.replace("\n", "").split(",")]

    for _ in range(80):
        for fish in registry:
            fish.tick()
    return len(registry)


# Fast approach :D
@expected_test_result(26984457539)
def solve2(input):
    fish = [0 for i in range(9)]
    for clock in input.replace("\n", "").split(","):
        fish[int(clock)] += 1

    for _ in range(256):
        spawners = fish.pop(0)
        fish.insert(6, spawners)
        fish[6] += fish.pop(7)
        fish.append(spawners)

    return sum(fish)
