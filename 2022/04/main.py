#!/usr/bin/env python3

import sys
import re


class Interval:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a}, {self.b})'

    # x @ y is True if the inteval [x1,x2] is within [y1,y2]
    def __matmul__(self, them):
        return them.a <= self.a and them.b >= self.b

    # x % y is True if the inteval [x1,x2] overlaps [y1,y2]
    def __mod__(self, them):
        return self.a <= them.b and them.a <= self.b


if __name__ == '__main__':
    match_pattern = re.compile(r'\d+')
    problem_input = sys.stdin.read().strip().split('\n')

    part_1_score = 0
    part_2_score = 0

    for line in problem_input:
        [a, b, c, d] = map(int, match_pattern.findall(line))
        x = Interval(a, b)
        y = Interval(c, d)

        if x @ y or y @ x:
            part_1_score += 1

        if x % y:
            part_2_score += 1

    print('Part 1:', part_1_score)
    print('Part 2:', part_2_score)
