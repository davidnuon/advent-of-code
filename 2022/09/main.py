#!/usr/bin/env python3

import sys
import enum
import dataclasses

@dataclasses.dataclass
class Point2D:
    x: int
    y: int
    
    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        return Point2D(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point2D(x=self.x - other.x, y=self.y - other.y)

    def __hash__(self):
        return hash(f'{self.x}, {self.y}')

    def is_normal_to(self, other):
        return self.x == other.x or self.y == other.y

    def copy(self):
        return Point2D(x=self.x, y=self.y)

class Direction(enum.Enum):
    UP = Point2D(0, -1)
    DOWN = Point2D(0, 1)
    LEFT = Point2D(-1, 0)
    RIGHT = Point2D(1, 0)

DIAGONALS = [
    Point2D(1, 1),
    Point2D(1, -1),
    Point2D(-1, 1),
    Point2D(-1, -1)
]

def process_sim(direciton, head, tail):
    new_head = head + direciton.value
    
    if new_head == tail:
        return new_head, tail.copy()
    if tail.is_normal_to(new_head):
        heading = head - tail
        if heading in DIAGONALS:
            new_tail = tail.copy()
        else:
            new_tail = head.copy()
    else:
        heading = new_head - tail
        if heading in DIAGONALS:
            new_tail = tail.copy()
        else:
            new_tail = head.copy()

    return new_head, new_tail


if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().splitlines()
    head = Point2D(x=0, y=0)
    tail = Point2D(x=0, y=0)
    touched_points = set()
    tailed_points = set()

    for line in problem_input:
        left, right = line.split(' ')
        direction_key, amount = left, int(right)

        match direction_key:
            case 'R':
                direction = Direction.RIGHT
            case 'L':
                direction = Direction.LEFT
            case 'U':
                direction = Direction.UP
            case 'D':
                direction = Direction.DOWN

        markers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'z', 'i', 'j', 'k', 'l', 'm']
        marker = 0
        for iteration in range(0, amount):
            head, tail = process_sim(direction, head, tail)
        
            touched_points.add(head)
            touched_points.add(tail)
            tailed_points.add(tail)

            rendered_points = set(
                map(lambda p: Point2D(x=p.x, y=p.y + 6), tailed_points)
            )
            
            # for y in range(0, 7):
            #     for x in range(0, 6):
            #         if (x, y) == (0, 6) and Point2D(x, y + 6) != tail:
            #             print('s', end='')
            #             continue
                
            #         if Point2D(x, y) == head + Point2D(x=0, y=6):
            #             print('H', end='')
            #             continue

            #         if Point2D(x, y) == tail + Point2D(x=0, y=6):
            #             print('T', end='')
            #             continue

            #         p = Point2D(x, y)
            #         marker = (marker + 1) % (markers.__len__() - 2)
            #         if p in rendered_points:
            #             print(markers[marker], end='')
            #             # print('.', end='')
            #         else: 
            #             print('.', end='')
            #     print()
            # print()
    print('Part 1:', len(tailed_points))