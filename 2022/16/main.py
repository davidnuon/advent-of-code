#!/usr/bin/env python3

from collections import defaultdict 
import itertools
import functools
import re

parse_pattern = re.compile('Valve (\w+) .*=(\d*); .* valves? (.*)')

@functools.cache
def find_max_pressure(maximum_time, starting_valve='AA', candidate_valves=frozenset(), elephant_friend=False):
    pressures = []
    """
        Enumerate all possible paths from the starting valve to the ending valves
        and find the maximum pressure that can be generated.

        We subtract the distance we calculated earlier from the maximum time.
    """
    for ending_valve in candidate_valves:
        path = starting_valve, ending_valve 
        if intervalve_distance[path] < maximum_time:
            remaining_time = maximum_time - intervalve_distance[path] - 1
            pressure = flow_rates[ending_valve] * remaining_time

            pressure += find_max_pressure(
                remaining_time, 
                ending_valve, 
                candidate_valves.difference({ending_valve}), 
            elephant_friend)
            pressures.append(pressure)
    
    elephant_pressure = 0

    if elephant_friend:
        elephant_pressure = find_max_pressure(26, candidate_valves=candidate_valves) 
    
    pressures.append(elephant_pressure)
    
    return max(pressures)

if __name__ == '__main__':
    valves = set()
    flow_rates = {}
    intervalve_distance = defaultdict(lambda: 1_000_000)

    with open('puzzle_input.txt') as f:
        for valve_name, flow_rate, children in parse_pattern.findall(f.read()):
            valves.add(valve_name)
            if flow_rate != '0':
                flow_rates[valve_name] = int(flow_rate)

            for child_valve in children.split(', '):
                intervalve_distance[child_valve, valve_name] = 1

    # Floyd-Warshall
    # Precompute the shortest path between any two valves
    # a is the start, b is the end, ab is the intermediate valve
    for ab, a, b in itertools.product(valves, valves, valves):   
        intervalve_distance[a, b] = min(intervalve_distance[a, b],
                                        intervalve_distance[a, ab] +
                                        intervalve_distance[ab, b]
                                        )

    print('Part 1:', find_max_pressure(30, candidate_valves=frozenset(flow_rates)))
    print('Part 2:', find_max_pressure(26, candidate_valves=frozenset(flow_rates), elephant_friend=True))
    