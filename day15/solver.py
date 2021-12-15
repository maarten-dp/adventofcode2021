from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

import hashlib

from runner_utils import expected_test_result


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

    def __iter__(self):
        return iter([self.priority, self.item])


class Node:
    def __init__(self, cost):
        self.cost = cost
        self.neighbours = []

    def register_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
        neighbour.neighbours.append(self)


class Grid:
    def __init__(self, lines):
        self.start = None
        rows = []
        for line in lines:
            row = []
            for x, value in enumerate(line):
                node = Node(value)
                if rows:
                    node.register_neighbour(rows[-1][x])
                if row:
                    node.register_neighbour(row[-1])
                row.append(node)
            rows.append(row)
        self.start = rows[0][0]
        self.end = node

    def find_cheapest_path(self):
        queue = PriorityQueue()
        queue.put(PrioritizedItem(0, self.start))
        cost = {self.start: 0}

        while not queue.empty():
            current_cost, node = queue.get()

            if node is self.end:
                return current_cost

            for neighbour in node.neighbours:
                new_cost = current_cost + neighbour.cost
                if neighbour not in cost or new_cost < cost[neighbour]:
                    cost[neighbour] = new_cost
                    queue.put(PrioritizedItem(new_cost, neighbour))



@expected_test_result(40)
def solve1(input):
    lines = [map(int, l) for l in input.split("\n") if l]
    return Grid(lines).find_cheapest_path()


@expected_test_result(315)
def solve2(input):
    lines = [list(map(int, l)) for l in input.split("\n") if l]

    rows = []
    for y in range(5):
        row = [[] for _ in range(len(lines))]
        for x in range(5):
            for idx, line in enumerate(lines):
                for value in line:
                    value += x + y
                    if value > 9:
                        value = (value % 10) + 1
                    row[idx].append(value)
        rows.extend(row)



    return Grid(rows).find_cheapest_path()
