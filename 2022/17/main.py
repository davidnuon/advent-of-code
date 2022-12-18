#!/usr/bin/env python3

from collections import defaultdict

class ZC(complex):

    def __iter__(self):
        yield int(self.real)
        yield int(self.imag)

    def __add__(self, other):
        return ZC(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return ZC(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return ZC(self.real * other.real, self.imag * other.imag)

shapes = [
    #  ####
    [
        ZC(0, 0),
        ZC(1, 0),
        ZC(2, 0),
        ZC(3, 0),
    ],

    # .#.
    # ###
    # .#.
    [
        ZC(1, 0),
        ZC(0, 1),
        ZC(1, 1),
        ZC(2, 1),
        ZC(1, 2),    
    ],

    # ..#
    # ..#
    # ###
    [
        ZC(0, 0),
        ZC(1, 0),
        ZC(2, 0),
        ZC(2, 1),
        ZC(2, 2)
    ],

    # #
    # #
    # #
    # #    
    [
        ZC(0, 0),
        ZC(0, 1),
        ZC(0, 2),
        ZC(0, 3)
    ],

    # ##
    # ##
    [
        ZC(0, 0),
        ZC(1, 0),
        ZC(0, 1),
        ZC(1, 1)
    ]
]

class Board:
    LEFT = ZC(-1, 0)
    RIGHT = ZC(1, 0)
    DOWN = ZC(0, -1)

    def __init__(self, move_directions):
        self.move_directions = move_directions
        self.move_idx = 0

        self.rocks = set()
        self.current_shape_idx = 0

        self.placement_count = 0

        self.shape_position = ZC(2, 3)

    def can_move_horizontal(self, direction):
        delta = Board.LEFT if direction == "<" else Board.RIGHT

        if (self.shape_position + delta).real in [-1, 7]:
            return False

        for block in shapes[self.current_shape_idx]:
            bp = block + self.shape_position + delta
            if bp in self.rocks or bp.real > 6:
                return False
        return True

    def can_move_down(self):
        delta = Board.DOWN

        if (self.shape_position + delta).imag < 0:
            return False

        for block in shapes[self.current_shape_idx]:
            bp = block + self.shape_position + delta
            if bp in self.rocks:
                return False

        return True

    def move(self):
        direction = self.move_directions[self.move_idx % len(self.move_directions)]
        self.move_idx = self.move_idx + 1
        if self.can_move_horizontal(direction) :
            if direction == "<":
                self.shape_position += Board.LEFT
            else:
                self.shape_position += Board.RIGHT

        if self.can_move_down():
            self.shape_position += Board.DOWN
        else:
            return True

        return False

    def drop(self):
        while True:
            if self.move():
                break
        self.place_piece()

    @property
    def height(self):
        return max(y for _, y in self.rocks)

    def place_piece(self):
        for block in shapes[self.current_shape_idx]:
            self.rocks.add(block + self.shape_position)

        self.placement_count += 1
        self.current_shape_idx = (self.current_shape_idx + 1) % len(shapes)
        self.shape_position = ZC(2, 3 + self.height + 1)

    def find_cycle(self):
        move_to_placement = defaultdict(list)
        heights = {}

        while True:
            self.drop()
            top = self.height

            heights[self.placement_count] = top + 1

            # Scan left to write if we see the same height again
            # 7 times
            if all(ZC(x, top) in self.rocks for x in range(7)):
                ending_move = (self.move_idx % len(self.move_directions), self.current_shape_idx)
                move_to_placement[ending_move].append(self.placement_count)

                # Once we see it again, we have a cycle
                if len(move_to_placement[ending_move]) == 2:
                    return move_to_placement[ending_move], heights

def part1(moves):
    board = Board(moves)

    for _ in range(2022):
        board.drop()
    print(f'Part 1: {board.height + 1}')

def part2(moves):
    board = Board(moves)
    placement_counts, heights = board.find_cycle()
    
    # First and second occurance of the cycle
    c1, c2 = placement_counts
    cycle_length = c2 - c1

    NUMBER_OF_PLACEMENTS = 1000000000000
    extra_placements = (NUMBER_OF_PLACEMENTS - c2) % cycle_length
    extra_height = heights[c1 + extra_placements] - heights[c1]

    cycles = (NUMBER_OF_PLACEMENTS - c1) // cycle_length
    cycle_height = heights[c2] - heights[c1]
    
    initial_height = heights[c1]

    total_cycle_height = cycle_height * cycles
    non_cycle_height =  initial_height + extra_height

    print(f'Part 2: {total_cycle_height + non_cycle_height}')

if __name__ == '__main__':
    moves = open("./puzzle_input.txt").read()
    part1(moves)
    part2(moves)

