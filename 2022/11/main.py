#!/usr/bin/env python3

import sys
import operator
import math

def parse_int(token):
    if not isinstance(token, str):
        return token

    digits = list(filter(str.isdigit, token))
    return int("".join(digits))

class MonkeyBlock:
    def __init__(self, monkey_number):
        self.monkey_number = monkey_number
        self.startng_items = []
        self.operation = ""
        self.test_items = {}
        self.test_predicate = []
        self.inspection_count = 0

    def throw_item(self, worry, worry_check = False):
        [_, opcode, right] = self.operation
        op = operator.add if opcode == '+' else operator.mul
        item = type(worry)(worry) * worry if right == 'old' else op(worry, int(right))
        if worry_check:
            item = item // 3
        divisor = int(self.test_predicate[-1])
        target_monkey = int(self.test_items[item % divisor == 0][-1])

        return (target_monkey, item)
    
    def inspect(self):
        self.inspection_count += 1

class ModularNumber:
    def __init__(self, worry):
        self.worry = worry
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        self.bases = { k: (worry % k) for k in primes }
 
    def __add__(self, other):
        for base in self.bases:
            self.bases[base] = self.bases[base] + (other % base)
        return self

    def __mul__(self, other):
        if isinstance(other, ModularNumber):
            for base in self.bases:
                self.bases[base] = self.bases[base] * (other.bases[base])
        else:
            for base in self.bases:
                self.bases[base] = self.bases[base] * (other % base)
        return self

    def __floordiv__(self, divisor):
        return self.bases[divisor] // divisor

    def __mod__(self, divisor):
        return self.bases[divisor] % divisor

    @staticmethod
    def from_string(token):
        return ModularNumber(parse_int(token))

def monkey_business(monkies, rounds, worry_check = False):
    hashed_monkies = {m.monkey_number: m for m in monkies}
    for _ in range(0, rounds):
        for monkey in monkies:
            while len(monkey.startng_items) > 0:
                item = monkey.startng_items.pop(0)
                (target_monkey, new_item) = monkey.throw_item(item, worry_check)                
                hashed_monkies[target_monkey].startng_items.append(new_item)
                monkey.inspect()

    return sorted([m.inspection_count for m in monkies])

def parse_monkeys(problem_input, number_handler = int):
    monkies = []
    for line in problem_input:
        tokens = line.split()
        first_token = tokens[0] if len(tokens) > 0 else ''
        current_monkey = monkies[-1] if len(monkies) > 0 else None
        match first_token:
            case 'Monkey':
                [_, number_token] = tokens
                monkey_number = int(number_token.replace(':', ''))
                monkies.append(MonkeyBlock(monkey_number))
            case 'Starting':
                current_monkey.startng_items = [number_handler(t) for t in tokens[2:]]
            case 'Operation:':
                current_monkey.operation = tokens[3:]
            case 'Test:':
                current_monkey.test_predicate = tokens[1:]
            case 'If':
                case_type = tokens[1].replace(':', '')
                current_monkey.test_items[case_type == 'true'] = tokens[2:]
    
    return monkies

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')

    part_1_scores = monkey_business(parse_monkeys(problem_input, number_handler=parse_int), 20, worry_check=True)
    part_2_scores = monkey_business(parse_monkeys(problem_input, number_handler=ModularNumber.from_string), 10000)
                     
    print(f'Part 1: {math.prod(part_1_scores[-2:])}')
    print(f'Part 2: {math.prod(part_2_scores[-2:])}')