from runner_utils import expected_test_result
from collections import defaultdict


class DeterministicDie:
    def __init__(self):
        self.roll_value = 100
        self.rolls = 0

    def roll(self):
        self.rolls += 1
        self.roll_value = (self.roll_value % 100) + 1
        return self.roll_value

    def consecutive_rolls(self, amount):
        for _ in range(amount):
            yield self.roll()


class Player:
    def __init__(self, name, position):
        self.name = f"Player {name}"
        self.position = position
        self.score = 0

    def move(self, spaces):
        self.position = ((self.position + spaces) % 10)
        if self.position == 0:
            self.position = 10
        self.score += self.position
        return self.position

    def __repr__(self):
        return self.name


class Board:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.die = DeterministicDie()
        self._current_player = 0

    def get_current_player(self):
        player = self.players[self._current_player]
        self._current_player = (self._current_player + 1) % 2
        return player

    def play_turn(self):
        player = self.get_current_player()
        spaces = sum(self.die.consecutive_rolls(3))
        player.move(spaces)
        if player.score >= 1000:
            return player


@expected_test_result(739785)
def solve1(input):
    lines = [l for l in input.split("\n") if l]
    p1 = Player(1, int(lines[0].split(": ")[-1]))
    p2 = Player(2, int(lines[1].split(": ")[-1]))

    board = Board(p1, p2)

    winner = None
    while not winner:
        winner = board.play_turn()

    loser = board.get_current_player()
    return board.die.rolls * loser.score


THRESHOLD = 21
RESULT = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}
WINNERS = {
    1: 0,
    2: 0,
}


class Position:
    def __init__(
        self,
        player1_turn,
        player1_position,
        player2_position,
        player1_score,
        player2_score,
        universes,
    ):
        self.player1_turn = player1_turn
        self.player1_position = player1_position
        self.player2_position = player2_position
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.universes = universes

    def move(self):
        position1 = self.player1_position
        score1 = self.player1_score
        position2 = self.player2_position
        score2 = self.player2_score

        for spaces, universes in RESULT.items():
            if self.player1_turn:
                position1 = (self.player1_position + spaces) % 10
                score1 = self.player1_score + position1 + 1
                if score1 >= THRESHOLD:
                    WINNERS[1] += self.universes * universes
                    continue
            else:
                position2 = (self.player2_position + spaces) % 10
                score2 = self.player2_score + position2 + 1
                if score2 >= THRESHOLD:
                    WINNERS[2] += self.universes * universes
                    continue

            yield Position(
                not self.player1_turn,
                position1,
                position2,
                score1,
                score2,
                self.universes * universes,
            )


@expected_test_result(444356092776315)
def solve2(input):
    lines = [l for l in input.split("\n") if l]
    p1 = int(lines[0].split(": ")[-1])
    p2 = int(lines[1].split(": ")[-1])

    positions = [Position(True, p1 - 1, p2 - 1, 0, 0, 1)]

    while positions:
        new_positions = []
        for position in positions:
            new_positions.extend(position.move())
        positions = new_positions
    return max(WINNERS.values())
