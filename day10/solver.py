from runner_utils import expected_test_result


CHUNK_DELIMITERS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

COMPLETION_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def get_scores(input):
    lines = [l for l in input.split("\n") if l]

    points = 0
    scores = []
    for statement in lines:
        stack = []
        is_valid = True
        for delimiter in statement:
            if delimiter in CHUNK_DELIMITERS.keys():
                stack.append(delimiter)
            else:
                chunk_start = stack.pop(-1)
                if delimiter != CHUNK_DELIMITERS[chunk_start]:
                    points += POINTS[delimiter]
                    is_valid = False
                    break
        if is_valid:
            score = 0
            for chunk_start in stack[::-1]:
                score *= 5
                score += COMPLETION_POINTS[CHUNK_DELIMITERS[chunk_start]]
            scores.append(score)
    idx = int(len(scores)/2)
    return points, sorted(scores)[idx]


@expected_test_result(26397)
def solve1(input):
    return get_scores(input)[0]


@expected_test_result(288957)
def solve2(input):
    return get_scores(input)[1]
