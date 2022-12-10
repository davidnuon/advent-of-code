#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')
    register = 1
    cycle = 0

    states = {}

    for line in problem_input:
        parts = line.split(' ')
        match parts[0]:
            case 'noop':
                states[cycle + 1] = register
                cycle += 1
            case 'addx':
                value = int(parts[1])
                states[cycle + 1] = register
                states[cycle + 2] = register

                cycle += 2
                register += value

    sample_idx = range(20, 240, 40)
    signal_sum = sum(map(lambda idx: idx * states[idx], sample_idx))
    
    print('Part 1:', signal_sum)
    WIDTH = 40 
    HEIGHT = 6
    pixels = [False] * (WIDTH * HEIGHT + 1)

    # The beam writes to the stream
    for cycle, register_x in enumerate(states.values()):
        pixel_position = cycle + 1
        beam_positon = cycle % 40

        if beam_positon in [register_x, register_x + 1, register_x - 1]:
            pixels[pixel_position] = True
    
    print('Part 2:')
    for idx, pixel in enumerate(pixels):
        if idx == 0:
            continue
        if pixel:
            print('⬛', end='')
        else:
            print('⬜', end='')

        if idx % WIDTH == 0:
            print()