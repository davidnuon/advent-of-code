#!/usr/bin/env python3

import sys
import re

def sand_sim(walls, max_depth, has_floor=True):
    # Walls and sand
    obstacles = walls.copy()

    # Sand flows from this point
    starting_sand = (500, 0)

    while True:
        # If the entry point is clogged (becomes an obstacle), stop
        if not has_floor and starting_sand in obstacles:
            return len(obstacles) - len(walls)

        sand_x, sand_y = starting_sand
        while True:
            if sand_y + 1 == max_depth:
                if has_floor:
                    return len(obstacles) - len(walls)
                else:
                    obstacles.add((sand_x, sand_y))
                    break
            if (sand_x, sand_y + 1) not in obstacles:
                """
                A unit of sand always falls down one step if possible. 
                If the tile immediately below is blocked (by rock or sand), 
                """
                sand_y += 1

            elif (sand_x - 1, sand_y + 1) not in obstacles:
                """
                the unit of sand attempts to instead move diagonally one step down 
                and to the left. 
                """
                sand_y += 1
                sand_x -= 1
            elif (sand_x + 1, sand_y + 1) not in obstacles:
                """
                If that tile is blocked, the unit of sand attempts 
                to instead move diagonally one step down and to the right. 
                """
                sand_y += 1
                sand_x += 1
            else:
                """
                Sand keeps moving as long as it is able to do so, at each step trying 
                to move down, then down-left, then down-right. 

                If all three possible destinations are blocked, 
                the unit of sand comes to rest and no longer moves, at which point the next unit 
                of sand is created back at the source.
                """
                obstacles.add((sand_x, sand_y))
                break

if __name__ == "__main__":
    coordinate_pattern = re.compile(r"(\d+),(\d+)")
    problem_input = sys.stdin.read().strip().split("\n")

    walls = set()
    max_depth = 0
    for line in problem_input:
        wall_coordinates = [
            list(map(int, w)) for w in coordinate_pattern.findall(line) 
        ]

        for idx in range(1, len(wall_coordinates)):
            x, y = map(int, wall_coordinates[idx])
            prev_x, prev_y = wall_coordinates[idx - 1]
            if y > max_depth or prev_y > max_depth:
                max_depth = max(y, prev_y)
            
            # Vertical wall
            if x == prev_x:
                for wall_y in range(min(y, prev_y), max(y, prev_y) + 1):
                    walls.add((x, wall_y))

            # Horizontal wall
            else:
                for wall_x in range(min(x, prev_x), max(x, prev_x) + 1):
                    walls.add((wall_x, y))
    
    max_depth += 1

    print("Part 1:", sand_sim(walls, max_depth, has_floor=True))
    print("Part 2:", sand_sim(walls, max_depth, has_floor=False))
