#!/usr/bin/env python3

import sys
import dataclasses

@dataclasses.dataclass
class Point3D:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        return Point3D(self.x * other, self.y * other, self.z * other)

    def __hash__(self):
        return hash(f'{(self.x, self.y, self.z)}')

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z



def get_adjacent(p):
    neighbors = [
        Point3D(-1, 0, 0),
        Point3D(1, 0, 0),
        Point3D(0, -1, 0),
        Point3D(0, 1, 0),
        Point3D(0, 0, -1),
        Point3D(0, 0, 1)
    ]    
    for n in neighbors:
        yield p + n

def in_bounds(P_min, P_max, p):
    return P_min.x <= p.x <= P_max.x and P_min.y <= p.y <= P_max.y and P_min.z <= p.z <= P_max.z

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().splitlines()
    points = set()
    for line in problem_input:
        x, y, z = map(int, line.split(','))
        points.add(Point3D(x, y, z))

    count = 0
    for p in points:
        for n in get_adjacent(p):
            if n not in points:
                count += 1

    print(f'Part 1: {count}')

    xs = [p.x for p in points]
    ys = [p.y for p in points]
    zs = [p.z for p in points]

    P_min = Point3D(min(xs) - 1, min(ys) - 1, min(zs) - 1)
    P_max = Point3D(max(xs) + 1, max(ys) + 1, max(zs) + 1)

    stack = [P_min]
    visited = set()
    surface_area = 0
    while stack:
        point = stack.pop()
        if point in visited:
            continue
        visited.add(point)
        for neighbor in get_adjacent(point):
            if neighbor in points:
                surface_area += 1

            if neighbor not in points and neighbor not in visited and in_bounds(P_min, P_max, neighbor):
                stack.append(neighbor)

    print(f'Part 2: {surface_area}')