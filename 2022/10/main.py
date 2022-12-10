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
        
    print(register, cycle)
    print()
    for k,v in states.states.items():
        print(f'Cycle {k}: {v[1]}')

    sample_idx = [20, 60, 100, 140, 180, 220]
    signal_sum = 0
    for idx in sample_idx:
        signal_strength = idx * states.states[idx][1]
        print(idx, states.states[idx][1], signal_strength)
        signal_sum += signal_strength

    print('Part 1:', signal_sum)        