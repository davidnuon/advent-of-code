#!/usr/bin/env python3

import sys
from enum import Enum


class Shape(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Result(Enum):
    Win = 6
    Draw = 3
    Lose = 0


# This shape -> beats this shape
WINNING_RULES = {
    Shape.Rock: Shape.Scissors,
    Shape.Paper: Shape.Rock,
    Shape.Scissors: Shape.Paper
}

# Inverse map of winning rules
LOSING_RULES = {v: k for (k, v) in WINNING_RULES.items()}


def calc_matchup(them, us):
    if them == us:
        return Result.Draw
    elif (them, us) in WINNING_RULES.items():
        return Result.Lose

    return Result.Win


def rps_encode(opponent, player):
    opp_map = {
        'A': Shape.Rock,
        'B': Shape.Paper,
        'C': Shape.Scissors,
        'X': Shape.Rock,
        'Y': Shape.Paper,
        'Z': Shape.Scissors
    }

    return [opp_map[opponent], opp_map[player]]


def needed_result_encode(code):
    result_map = {
        'X': Result.Lose,
        'Y': Result.Draw,
        'Z': Result.Win
    }

    return result_map[code]


if __name__ == '__main__':
    problem_input = sys.stdin.read().strip().split('\n')
    plays = [line.split(' ') for line in problem_input]

    part_1_points = 0
    part_2_points = 0

    for play in plays:
        [them, us] = rps_encode(*play)
        result = calc_matchup(them, us)

        part_1_points += result.value + us.value

        needed_result = needed_result_encode(play[1])

        match needed_result:
            case Result.Win:
                needed_play = LOSING_RULES[them]

            case Result.Lose:
                needed_play = WINNING_RULES[them]

            case Result.Draw:
                needed_play = them

        part_2_points += needed_result.value + needed_play.value

    print('Part 1:', part_1_points)
    print('Part 2:', part_2_points)
