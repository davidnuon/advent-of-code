#!/usr/bin/env python3.10

import sys


def rps_encode(opponent, player):
    opp_map = {
        'A': 'Rock',
        'B': 'Paper',
        'C': 'Scissors'
    }

    player_map = {
        'X': 'Rock',
        'Y': 'Paper',
        'Z': 'Scissors'
    }

    return [opp_map[opponent], player_map[player]]


def calc_rps_result(opponent, player):
    match [opponent, player]:
        case [opponent, 'Rock']:
            return 1 + ({
                'Rock': 3,
                'Paper': 0,
                'Scissors': 6
            })[opponent]
        case [opponent, 'Paper']:
            return 2 + ({
                'Rock': 6,
                'Paper': 3,
                'Scissors': 0
            })[opponent]
        case [opponent, 'Scissors']:
            return 3 + ({
                'Rock': 0,
                'Paper': 6,
                'Scissors': 3
            })[opponent]


def calc_matchup(left, right):
    opponent_play = rps_encode(left, right)[0]
    player_play = None
    match [opponent_play, right]:
        # Lose
        case [opponent, 'X']:
            player_play = ({
                'Rock': 'Scissors',
                'Paper': 'Rock',
                'Scissors': 'Paper'
            })[opponent]
        # Draw
        case [opponent, 'Y']:
            player_play = ({
                'Rock': 'Rock',
                'Paper': 'Paper',
                'Scissors': 'Scissors'
            })[opponent]

        # Win
        case [opponent, 'Z']:
           player_play = ({
                'Scissors': 'Rock',
                'Rock': 'Paper',
                'Paper': 'Scissors'
            })[opponent]

    return [opponent_play, player_play]

if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')
    plays = [line.split(' ') for line in problem_input]

    part_1_points = 0
    part_2_points = 0

    for [left, right] in plays:
        part_1_points += calc_rps_result(*rps_encode(left, right))
        part_2_points += calc_rps_result(*calc_matchup(left, right))

    print('Part 1:', part_1_points)
    print('Part 2:', part_2_points)