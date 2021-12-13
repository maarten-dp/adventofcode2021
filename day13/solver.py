from runner_utils import expected_test_result


def fold(axis, num, coords):
    folded = set()
    idx = 0 if axis == 'x' else 1
    for coord in coords:
        coord = list(coord)
        val = coord[idx]
        if val > num:
            coord[idx] = num - (val - num)
        folded.add(tuple(coord))
    return folded


def parse_instructions(input):
    coordinates = [l for l in input.split("\n") if l]
    coords = []
    fold_instructions = []
    for coordinate in coordinates:
        if "," in coordinate:
            coords.append([int(c) for c in coordinate.split(",")])
        else:
            axis, num = coordinate.replace('fold along ', '').split('=')
            fold_instructions.append((axis, int(num)))
    return coords, fold_instructions


@expected_test_result(17)
def solve1(input):
    coordinates, fold_instructions = parse_instructions(input)
    axis, num = fold_instructions[0]
    return len(fold(axis, num, coordinates))


@expected_test_result("""#####
#...#
#...#
#...#
#####""")
def solve2(input):
    coords, fold_instructions = parse_instructions(input)
    for axis, num in fold_instructions:
        coords = fold(axis, num, coords)

    max_y = max([y for _, y in coords])
    max_x = max([x for x, _ in coords])

    rows = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            if (x, y) in coords:
                row.append("#")
            else:
                row.append(".")
        rows.append("".join(row))
    return "\n".join(rows)
