#!/usr/bin/env python3

import sys

def find_marker_index(stream, marker_size = 4):
    window_size = marker_size - 1

    for idx in range(window_size, len(stream)):
        start = idx-window_size
        end = idx+1
        substring = stream[start:end]

        if len(set(substring)) == marker_size:
            return idx+1
    return None

if __name__ == '__main__':    
    problem_input = sys.stdin.read().strip()

    print('Part 1:', find_marker_index(problem_input))
    print('Part 2:', find_marker_index(problem_input, marker_size=14))