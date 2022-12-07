#!/usr/bin/env python3

import sys
import enum

class CommandType(enum.Enum):
    LS = 0
    CD = 1

class Node:
    class NodeType(enum.Enum):
        FILE = 0
        DIRECTORY = 1

    def __init__(self, name, node_type, parent, size = 0):
        self.name = name
        self.node_type = node_type
        self.children = {}
        self.size = size
        self.parent = parent

    def get_size(self):
        if self.node_type == Node.NodeType.FILE:
            return self.size
        else:
            return sum([child.get_size() for child in self.children.values()])

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
            case _:
                raise ValueError(f'Unknown command: {command_exec}')
    
        return Command(command, command_exec, command_args)

if __name__ == '__main__':
    # Parse input
    commands = []
    problem_input = sys.stdin.read().strip().split('\n')

    for line in problem_input:
        if line.startswith('$'):
            command = Command.parse_command(line[2:])
            commands.append(command)
        else:
            commands[-1].runtime.append(line)
    
    # Build tree
    node = Node('/', Node.NodeType.DIRECTORY, None)
    root = node
    current_node = node

    for c in commands:
        match c.command_exec:
            case CommandType.LS:
                for line in c.runtime:
                    [left, right] = line.split(' ')
                    match left:
                        case 'dir':
                            current_node.children[right] = Node(right, Node.NodeType.DIRECTORY, current_node)
                        case _:
                            current_node.children[right] = Node(right, Node.NodeType.FILE, current_node, size = int(left))
            case CommandType.CD:
                next_directory = c.command_args[0]
                match next_directory:
                    case '..':
                        current_node = current_node.parent
                    case '/':
                        current_node = root
                    case _:
                        if next_directory in current_node.children:
                            current_node = current_node.children[next_directory]
                        else:
                            raise ValueError(f'No such directory: {next_directory}')

    # Build arrays used for Part 1 and 2
    nodes = [root]
    part_1_directories = []
    part_2_directories = []
    
    SMALL_SIZE = 100_000    
    while len(nodes) > 0:
        node = nodes.pop()
 
        if node.node_type == Node.NodeType.DIRECTORY:
            if node.get_size() < SMALL_SIZE:
                part_1_directories.append(node)
            part_2_directories.append(node)
        for child in node.children.values():
            nodes.append(child)

    print('Part 1:', sum(c.get_size() for c in part_1_directories))
    
    TOTAL_SPACE = 70_000_000
    UNUSED_SPACE = 30_000_000
    TARGET_SPACE = TOTAL_SPACE - UNUSED_SPACE
    ROOT_SIZE = root.get_size()
    
    for d in sorted(part_2_directories, key = lambda d: d.get_size()):
        if d == root:
            continue
        if ROOT_SIZE - d.get_size() < TARGET_SPACE:
            print('Part 2:', d.get_size())
            break