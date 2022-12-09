#!/usr/bin/env python3

import sys
import dataclasses

@dataclasses.dataclass
class Point2D:
    x: int
    y: int

    def __add__(self, other):
        return Point2D(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point2D(x=self.x - other.x, y=self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def is_next_to(self, other):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def sign(self):
        return Point2D(x=self.__sign(self.x), y=self.__sign(self.y))

    def __sign(self, x):
        return (x > 0) - (x < 0)

DIRECTIONS = {
    'U': Point2D(x=0, y=-1),
    'D': Point2D(x=0, y=1),
    'L': Point2D(x=-1, y=0),
    'R': Point2D(x=1, y=0)
}

def sim_step(rope, head_idx, tail_idx):
    tail = rope[tail_idx]
    head = rope[head_idx]

    if not tail.is_next_to(head):
        rope[tail_idx] += (head - tail).sign()

def rope_sim(problem_input, knot_size=2):
    rope = [Point2D(0, 0) for _ in range(0, knot_size)]
    tailed_points = set()

    for line in problem_input:
        left, right = line.split(' ')
        direction_key, amount = left, int(right)
        direction = DIRECTIONS[direction_key]

        for _ in range(0, amount):
            rope[0] = rope[0] + direction
            for idx in range(1, knot_size):
                sim_step(rope, idx - 1, idx)

            tailed_points.add(rope[-1])
    return len(tailed_points)

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().splitlines()

    print('Part 1:', rope_sim(problem_input, knot_size=2))
    print('Part 2:', rope_sim(problem_input, knot_size=10))