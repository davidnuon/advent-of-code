#!/usr/bin/env python3

import sys
import functools

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')
    
    height_map = {}

    @functools.cache
    def is_visible(point, boundery):
        (x, y) = point
        (X_BOUNDERY, Y_BOUNDERY) = boundery

        if x == 0 or x == (X_BOUNDERY - 1)\
            or y == 0 or y == (Y_BOUNDERY -1):
                return True
        
        F = lambda KPs : all(height_map[coord] < height_map[point] for coord in KPs if coord in height_map)

        neighbors_coords = [
            F([(x - k, y) for k in range(1, x+1)]),
            F([(x, y - k) for k in range(1, y+1)]),
            F([(x + k, y) for k in range(1, X_BOUNDERY - 1)]),
            F([(x, y + k) for k in range(1, Y_BOUNDERY - 1)])
        ]

        return any(neighbors_coords)

    i,j = [0, 0]

    for lines in problem_input:
        i = 0
        for char in lines:
            height_map[(i, j)] = int(char)
            i += 1
        j += 1

    X_BOUNDERY = i
    Y_BOUNDERY = j

    part_1_score = 0
    for (x,y) in height_map:
        if is_visible((x,y), (X_BOUNDERY, Y_BOUNDERY)):
            part_1_score += 1
   
    print(part_1_score)