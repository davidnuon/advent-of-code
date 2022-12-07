#!/usr/bin/env python3

import sys
import enum

class CommandType(enum.Enum):
    LS = 0
    CD = 1
    DIR = 3

class Command:
    def __init__(self, command, command_exec, command_args = []):
        self.command = command
        self.runtime = []
        self.command_exec = command_exec
        self.command_args = command_args

    def __str__(self):
        return f'{self.command} {self.runtime}'

    def __repr__(self):
        return f'{self.command} {self.runtime}'

    @staticmethod
    def parse_command(command):
        tokens = command.split(' ')
        command_exec = tokens[0]
        command_args = tokens[1:]

        match command_exec:
            case 'ls':
                command_exec = CommandType.LS
            case 'cd':
                command_exec = CommandType.CD
            case 'dir':
                command_exec = CommandType.DIR
            case _:
                raise ValueError(f'Unknown command: {command_exec}')
    
        return Command(command, command_exec, command_args)

if __name__ == '__main__':    
    commands = []
    problem_input = sys.stdin.read().strip().split('\n')

    for line in problem_input:
        if line.startswith('$'):
            command = Command.parse_command(line[2:])
            commands.append(command)
        else:
            commands[-1].runtime.append(line)

    for c in commands:
        print(c.command)
        for r in c.runtime:
            print(f'\t{r}')

        