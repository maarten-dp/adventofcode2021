from runner_utils import expected_test_result

def parse(data):
    return [int(d) for d in data.split("\n") if d]


def get_previous_highs(numbers):
    previous = numbers[0]
    larger = 0
    for number in numbers[1:]:
        if number > previous:
            larger += 1
        previous = number
    return larger


@expected_test_result(7)
def solve1(input):
    return get_previous_highs(parse(input))


@expected_test_result(5)
def solve2(input):
    input = parse(input)
    sums = []
    for idx in range(len(input) - 2):
        sums.append(sum(input[idx:idx+3]))
        previous = input[0]

    return get_previous_highs(sums)
