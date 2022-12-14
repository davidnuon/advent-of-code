#!/usr/bin/env python3

import sys

def is_visible(point, boundery):
    (x, y) = point
    (X_BOUNDERY, Y_BOUNDERY) = boundery

    if x == 0 or x == (X_BOUNDERY - 1) or y == 0 or y == (Y_BOUNDERY - 1):
        return True

    def has_visibile_neighbors(coords): return all(
        height_map[coord] < height_map[point] for coord in coords if coord in height_map)

    neighbors_coords = [
        has_visibile_neighbors([(x - k, y) for k in range(1, x+1)]),
        has_visibile_neighbors([(x, y - k) for k in range(1, y+1)]),
        has_visibile_neighbors([(x + k, y) for k in range(1, X_BOUNDERY - 1)]),
        has_visibile_neighbors([(x, y + k) for k in range(1, Y_BOUNDERY - 1)])
    ]

    return any(neighbors_coords)


def calculate_scenic_score(point, boundery):
    (x, y) = point
    (X_BOUNDERY, Y_BOUNDERY) = boundery

    up_score = 0
    for k in range(1, y+1):
        up_score += 1
        if height_map[(x, y - k)] >= height_map[point]:
            break

    down_score = 0
    for k in range(1, Y_BOUNDERY):
        if (x, y + k) not in height_map:
            continue

        down_score += 1
        if height_map[(x, y + k)] >= height_map[point]:
            break

    left_score = 0
    for k in range(1, x+1):
        left_score += 1
        if height_map[(x - k, y)] >= height_map[point]:
            break

    right_score = 0
    for k in range(1, X_BOUNDERY):
        if (x + k, y) not in height_map:
            continue

        right_score += 1
        if height_map[(x + k, y)] >= height_map[point]:
            break

    return up_score * down_score * left_score * right_score


if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')

    height_map = {}
    i, j = [0, 0]

    for lines in problem_input:
        i = 0
        for char in lines:
            height_map[(i, j)] = int(char)
            i += 1
        j += 1

    X_BOUNDERY = i
    Y_BOUNDERY = j

    part_1_score = 0
    part_2_score = -1
    out = {}
    for (x, y) in height_map:
        if is_visible((x, y), (X_BOUNDERY, Y_BOUNDERY)):
            part_1_score += 1
        part_2_score = max(part_2_score, calculate_scenic_score(
            (x, y), (X_BOUNDERY, Y_BOUNDERY)))

    print('Part 1:', part_1_score)
    print('Part 2:', part_2_score)
