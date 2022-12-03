#!/usr/bin/env python3

import sys

def calc_value(letter):
    ordinal = ord(letter)
    ordinal_lowercase_z = ord('z')
    ordinal_uppercase_z = ord('Z')

    if letter.islower():
        return ordinal - ordinal_lowercase_z + 26
        
    return (ordinal - ordinal_uppercase_z) + 26 + 26 

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')
    
    part_one_score = 0
    for line in problem_input:
        left = set(line[:len(line)//2])
        right = set(line[len(line)//2:])
        common = list(left.intersection(right))[0]
        part_one_score += calc_value(common)
    
    print('Part 1:', part_one_score)

    part_two_score = 0
    elf_squad_size = 3
    for i in range(0, len(problem_input), elf_squad_size):
        squad = [set(s) for s in problem_input[i:i + elf_squad_size]]
        common = squad[0]
        for elf_bag in squad[1:]:
            common = common.intersection(elf_bag)
        part_two_score += calc_value(list(common)[0])

    print('Part 2:', part_two_score)

