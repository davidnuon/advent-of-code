#!/usr/bin/env python3

import sys
import enum
import dataclasses

@dataclasses.dataclass
class Point2D:
    x: int
    y: int

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))

def get_map(problem_input):
    height_map = {}
    target_node = None
    x, y = 0, 0
    for line in problem_input:
        x = 0
        for char in line:
            point = Point2D(x, y)
            height_map[point] = ord(char) - 97
            if char == 'S':
                height_map[point] = 0
            if char == 'E':
                target_node = point
                height_map[point] = 24
            x += 1
        y += 1
    
    return height_map, target_node, x, y

class Directions(enum.Enum):
    UP = Point2D(0, -1)
    DOWN = Point2D(0, 1)
    LEFT = Point2D(-1, 0)
    RIGHT = Point2D(1, 0)

def find_path(height_map, start, target):
    queue = [start]
    visited = set()
    parent = {}
    while queue:
        current = queue.pop(0)
        if current == target:
            break
        for direction in Directions:
            new_point = current + direction.value
            if new_point in height_map and height_map[new_point] - height_map[current] <= 1:
                if new_point not in visited:
                    queue.append(new_point)
                    visited.add(new_point)
                    parent[new_point] = current
    path = []
    current = target
    if current not in parent:
        return []
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path


if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')
    height_map, target, WIDTH, HEIGHT = get_map(problem_input)

    # Part 1
    path = find_path(height_map, Point2D(0, 0), target)
    print(f'Part 1: {len(path) - 1}')
    
    # Part 2
    height_map[target] = ord('z') - 97
    starting_points = []
    for point, height in height_map.items():
        if height == 0:
            starting_points.append(point)
    
    path_lengths = [ len(find_path(height_map, starting_point, target)) for starting_point in starting_points ]
    print(f'Part 2: {min([l for l in path_lengths if l > 0]) - 1}')