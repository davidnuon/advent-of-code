#!/usr/bin/env python3

import sys
from dataclasses import dataclass


class CPUStates:
    def __init__(self):
        self.states = {}

    def add_state(self, cycle, register):
        self.states[cycle] = (cycle, register)

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')
    register = 1
    cycle = 0

    states = CPUStates()

    for line in problem_input:
        parts = line.split(' ')
        match parts[0]:
            case 'noop':
                states.add_state(cycle + 1, register)
                cycle += 1
            case 'addx':
                value = int(parts[1])
                states.add_state(cycle + 1, register)
                states.add_state(cycle + 2, register)

                cycle += 2
                register += value

    sample_idx = [20, 60, 100, 140, 180, 220]
    signal_sum = 0
    for idx in sample_idx:
        signal_strength = idx * states.states[idx][1]
        signal_sum += signal_strength
    
    print('Part 1:', signal_sum)

    memory_states = [s[1] for s in states.states.values()]
    pixels = [False] * (40 * 6 + 1)

    for _c, register_x in enumerate(memory_states):
        cycle = _c + 1
        beam_positon = _c % 40

        if beam_positon in [register_x, register_x + 1, register_x - 1]:
            pixels[cycle] = True
    
    print('Part 2:')
    for idx, pixel in enumerate(pixels):
        if idx == 0:
            continue
        if pixel:
            print('⬛', end='')
        else:
            print('⬜', end='')

        if idx % 40 == 0:
            print()