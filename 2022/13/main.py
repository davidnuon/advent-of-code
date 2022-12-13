#!/usr/bin/env python3

import sys
import json
from itertools import zip_longest

def validate(left, right):
    match (type(left).__name__, type(right).__name__):
        case ('list', 'list'):
            items = zip_longest(left, right)
            for (left_item, right_item) in items:
                result = validate(left_item, right_item)
                if result is not None:
                    return result
            return validate(len(left), len(right))
        case ('int', 'int'):
            if left == right:
                return None
            return left < right
        case ('list', 'int'):
            return validate(left, [right])
        case ('int', 'list'):
            return validate([left], right)


if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n\n')
    problem_pairs = [[json.loads(p) for p in line.split('\n')]
                     for line in problem_input]

    correct_pairs = [
        (idx + 1) for idx, pair in enumerate(problem_pairs) if validate(pair[0], pair[1])]
    packets = [p for pair in problem_pairs for p in pair]

    print('Part 1:', sum(correct_pairs))

    """
    The first divider packet is 1 + the number of packets that come before it
    The second divider packet is 2 + the number of packets that come before it
    (+ 2) because the second divider comes after the first divider
    """

    divider_1 = 1 + sum(1 for p in packets if validate(p, [[2]]))
    divider_2 = 2 + sum(1 for p in packets if validate(p, [[6]]))
    print('Part 2:', divider_1 * divider_2)