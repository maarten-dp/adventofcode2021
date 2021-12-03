from runner_utils import expected_test_result


@expected_test_result(198)
def solve1(input):
    lines = [l for l in input.split('\n') if l]
    threshold = len(lines) / 2
    gamma = []
    epsilon = []

    for values in zip(*lines):
        if sum(map(int, values)) > threshold:
            gamma.append('1')
            epsilon.append('0')
        else:
            gamma.append('0')
            epsilon.append('1')
    return int("".join(gamma), 2) * int("".join(epsilon), 2)


def get_value(lines, depth, key1, key2):
    threshold = len(lines) / 2
    if threshold < 1:
        return int(lines[0], 2)

    values = [int(l[depth]) for l in lines]
    if sum(values) >= threshold:
        lines = [l for l in lines if l[depth] == key1]
    else:
        lines = [l for l in lines if l[depth] == key2]
    return get_value(lines, depth + 1, key1, key2)


@expected_test_result(230)
def solve2(input):
    lines = [l for l in input.split('\n') if l]

    oxygen = get_value(lines, 0, "1", "0")
    co2 = get_value(lines, 0, "0", "1")
    return oxygen * co2
