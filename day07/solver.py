from runner_utils import expected_test_result


class Ranking:
    def __init__(self, max, costs):
        self.max = max
        self.ranking = {i: 0 for i in range(max + 1)}
        self.costs = costs

    def add_number(self, number):
        for i in range(self.max + 1):
            self.ranking[i] += self.costs[abs(number - i)]

    def get_lowest_cost_number(self):
        key = min(self.ranking.values())
        return {v: k for k, v in self.ranking.items()}[key]

    def get_lowest_fuel_cost(self, numbers):
        fuel = 0
        reference_number = self.get_lowest_cost_number()
        for number in numbers:
            fuel += self.costs[abs(reference_number - number)]
        return fuel


def calculate_lowest_cost(numbers, cost_mapping):
    ranking = Ranking(max(numbers), cost_mapping)
    for number in numbers:
        ranking.add_number(number)
    return ranking.get_lowest_fuel_cost(numbers)


@expected_test_result(37)
def solve1(input):
    numbers = [int(i) for i in input.replace("\n", "").split(",")]
    cost_mapping = {i: i for i in range(max(numbers) + 1)}
    return calculate_lowest_cost(numbers, cost_mapping)


@expected_test_result(168)
def solve2(input):
    numbers = [int(i) for i in input.replace("\n", "").split(",")]

    cost_mapping = {}
    cumul = 0
    for i in range(max(numbers) + 1):
        cumul += i
        cost_mapping[i] = cumul

    return calculate_lowest_cost(numbers, cost_mapping)
