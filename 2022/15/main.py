#!/usr/bin/env python3

import re
from itertools import pairwise

number_pattern = re.compile(r'(-?\d+)')

def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def diamond_corner_points(point, distance):
    x, y = point

    return [
        ( (pair[0][0] + x, pair[0][1] + y), (pair[1][0] + x, pair[1][1] + y))
        for pair in
        [
            [(-distance, 0), (0, distance)],
            [(0, distance), (distance, 0)],
            [(distance, 0), (0, -distance)],
            [(0, -distance), (-distance, 0)],
        ]
    ]

def manhattan_intersection(point, distance, y_line=10):
    x, y = point

    line_pairs = [
        [ (pair[0][0] + x, pair[0][1] + y), (pair[1][0] + x, pair[1][1] + y)]
        for pair in
        [
            [(-distance, 0), (0, distance)],
            [(0, distance), (distance, 0)],
            [(distance, 0), (0, -distance)],
            [(0, -distance), (-distance, 0)],
        ]
    ]

    for line_pair in line_pairs:
        p1, p2 = line_pair
        x1, y1 = p1
        x2, y2 = p2

        if y_line < max(y1, y2) and y_line > min(y1, y2):
            x_intersection = x1 + (y_line - y1) * (x2 - x1) // (y2 - y1)
            yield (x_intersection, y_line)

def part_1(problem_input):
    line_points = set()
    for line in problem_input:
        numbers = number_pattern.findall(line)
        cx, cy, rx, ry = map(int, numbers)
        distance = manhattan_distance((cx, cy), (rx, ry))
        y_line = 2_000_000
        intersection_points = [p[0]
                               for p in manhattan_intersection((cx, cy), distance, y_line)]
        if len(intersection_points) > 1:
            for p in range(min(intersection_points), max(intersection_points)):
                line_points.add((p, y_line))
        elif len(intersection_points) == 1:
            line_points.add((intersection_points[0], y_line))

    print(f'Part 1: {len(line_points)}')

def part_2(problem_input):
    MAX_DIM = 4_000_000
    coordinate_to_sensor_range = {}
    
    for line in problem_input:
        numbers = number_pattern.findall(line)
        cx, cy, rx, ry = map(int, numbers)
        distance = manhattan_distance((cx, cy), (rx, ry))
        coordinate_to_sensor_range[(cx, cy)] = distance

    # Scan through each through each y-line, looking for areas where the
    # sensor can see the beacon
    for y_line in range(0, MAX_DIM):
        intervals = []
        for (sx, sy), distance in coordinate_to_sensor_range.items():
            # If the sensor's y distance is non-zero
            dy = abs(sy - y_line)
            if distance > dy:

                # This is the x-distance of the manhattan distance
                dx = distance - dy

                # Then add the interval to the list of intervals
                # The interval is (a, b)
                # The interval is a hoirzontal line, a slice of all the diamonds
                # Where a is the left-most x-coordinate of the interval
                # And b is the right-most x-coordinate of the interval

                a = max(0, sx - dx)
                b = min(MAX_DIM + 1, sx + dx + 1)
                intervals.append((a, b))
        
        if len(intervals) == 0:
            continue

        # Pad intervals with a dummy interval at the end
        # Each interval is an interval of horizontalline segments
        # Sort each pair by its start
        intervals = sorted(intervals) + [(MAX_DIM, MAX_DIM + 10)]
        
        largest_left_hand_end = 0
        # Iterate through the list of intervals, two at a time
        for pair in pairwise(intervals):
            (_, current_end), (next_start, _) = pair
            largest_left_hand_end = max(largest_left_hand_end, current_end)

            # If the intervals are disjoint, the gap is where the sesnors 
            # can't reach
            if largest_left_hand_end < next_start:
                print('Part 2:', largest_left_hand_end * MAX_DIM + y_line)
                return


if __name__ == '__main__':
    with open('./puzzle_input.txt') as f:
        problem_input = f.read().strip().split('\n')
    part_1(problem_input)
    part_2(problem_input)
