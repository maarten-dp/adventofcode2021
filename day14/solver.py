from collections import Counter
from collections import defaultdict

from runner_utils import expected_test_result


def parse_input(input):
    lines = [l for l in input.split("\n") if l]
    mapping = dict([l.split(" -> ") for l in lines[1:]])
    template = list(lines[0])
    return mapping, template


# Naive approach ;)
@expected_test_result(1588)
def solve1(input):
    mapping, template = parse_input(input)

    for _ in range(10):
        snapshot = template[:]
        for idx in range(len(template)):
            key = "".join(snapshot[idx:idx+2])
            if len(key) == 1:
                continue
            insert_index = (idx * 2) + 1
            template.insert(insert_index, mapping[key])

    counts = [v for v in Counter(template).values()]
    return max(counts) - min(counts)


# Fast approach :D
@expected_test_result(2188189693529)
def solve2(input):
    mapping, template = parse_input(input)

    pairs = defaultdict(lambda: 0)
    element_counts = defaultdict(lambda: 0)
    element_counts.update({e: 1 for e in template})

    # bootstrap the pairs
    for idx in range(len(template)):
        key = "".join(template[idx:idx+2])
        if len(key) == 1:
            continue
        pairs[key] += 1

    # calculate the steps
    for _ in range(40):
        pair_growth = defaultdict(lambda: 0)
        for key in list(pairs.keys()):
            element = mapping[key]
            amount = pairs[key]
            element_counts[element] += amount
            pair_growth[f"{key[0]}{element}"] += amount
            pair_growth[f"{element}{key[1]}"] += amount
        pairs = pair_growth

    return max(element_counts.values()) - min(element_counts.values())
