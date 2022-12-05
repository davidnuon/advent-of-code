#!/usr/bin/env python3

import sys
import re
import enum

class ParsingState(enum.Enum):
    Crate = 1
    Instructions = 2

class StackCollection:
    def __init__(self, size):
        self.size = size
        self.stacks = [list() for _ in range(0, size)]

    # Move an amount of crates from one stack to another
    # but moving them one at a time
    def move_with_pop(self, src, dst, amount):
        self.stacks[dst] = self.stacks[dst] + self.stacks[src][-amount:][::-1]
        self.stacks[src] = self.stacks[src][:-amount]

    # Move an amount of crates from one stack to another
    # but moving multiple crates at a time
    def move_with_substack(self, src, dst, amount):
        self.stacks[dst] = self.stacks[dst] + self.stacks[src][-amount:]
        self.stacks[src] = self.stacks[src][:-amount]

if __name__ == '__main__':
    number_pattern = re.compile(r'\d+')
    move_pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    
    problem_input = sys.stdin.read().split('\n')

    crates = []
    instructions = []

    # Parsing data
    parsing_state = ParsingState.Crate
    for line in problem_input:
        if line == '':  
            parsing_state = ParsingState.Instructions
            continue

        match parsing_state:
            case ParsingState.Crate:
                crates.append(line)
            case ParsingState.Instructions:
                instructions.append(line)

    data_positions = []
    for i in number_pattern.finditer(crates[-1]):
        data_positions.append(i.start())

    part_1_stacks = StackCollection(len(data_positions))
    part_2_stacks = StackCollection(len(data_positions))
    
    # Create identical stacks collections for part 1 and 2
    for c in crates[:-1]:
        crate_string = f'{c:{len(crates[-1])}}'
        for idx, crate_string_idx in enumerate(data_positions):
            item = crate_string[crate_string_idx]
            if item != ' ':
                part_1_stacks.stacks[idx].insert(0, item)
                part_2_stacks.stacks[idx].insert(0, item)
    
    # Execeute instructions
    for instruction in instructions:
        [amount, src, dst] = map(int, move_pattern.match(instruction).groups())
        part_1_stacks.move_with_pop(src-1, dst-1, amount)
        part_2_stacks.move_with_substack(src-1, dst-1, amount)

    print('Part 1:', ''.join([s[-1] for s in part_1_stacks.stacks]))
    print('Part 2:', ''.join([s[-1] for s in part_2_stacks.stacks]))
