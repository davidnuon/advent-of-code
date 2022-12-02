#!/usr/bin/env python3

import os
import sys

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')
    sacks = [0]
    for line in problem_input:
        if line == '':
            sacks.append(0)
        else:
            sacks[-1] = sacks[-1] + int(line)

    print('Part 1:', max(sacks))
    print('Part 2:', sum(sorted(sacks)[-3:]))