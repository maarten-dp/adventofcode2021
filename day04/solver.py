from collections import defaultdict

from runner_utils import expected_test_result


class BingoCard:
    def __init__(self, raw_numbers):
        self.grid = [[]] * 5

        self.numbers = {}
        self.unmarked_sum = 0

        self.x_marks = defaultdict(lambda: 0)
        self.y_marks = defaultdict(lambda: 0)

        self.won = False
        self._populate_grid(raw_numbers)

    def _populate_grid(self, raw_numbers):
        for y, row in enumerate(raw_numbers):
            for x, value in enumerate(row):
                self.numbers[value] = (x, y)
                self.grid[y].append(value)
            self.unmarked_sum += sum(row)

    def mark_number(self, value):
        if value not in self.numbers:
            return

        self.unmarked_sum -= value

        x, y = self.numbers[value]
        self.x_marks[x] += 1
        self.y_marks[y] += 1

        if self.x_marks[x] == 5 or self.y_marks[y] == 5:
            return value


def parse_input(input):
    lines = input.split("\n")
    numbers = [int(l) for l in lines[0].split(",")]
    cards = []
    card_numbers = []
    for line in lines[2:]:
        if not line:
            cards.append(BingoCard(card_numbers))
            card_numbers = []
        else:
            card_numbers.append([int(l) for l in line.split(" ") if l])
    return numbers, cards


@expected_test_result(4512)
def solve1(input):
    numbers, cards = parse_input(input)
    for number in numbers:
        for card in cards:
            bingo_sum = card.mark_number(number)
            if bingo_sum:
                return bingo_sum * card.unmarked_sum


@expected_test_result(1924)
def solve2(input):
    numbers, cards = parse_input(input)
    last_winning_value = None
    for number in numbers:
        for card in cards:
            bingo_sum = card.mark_number(number)
            if bingo_sum and not card.won:
                card.won = True
                last_winning_value = bingo_sum * card.unmarked_sum
    return last_winning_value
