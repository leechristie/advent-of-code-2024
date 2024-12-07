# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time

from grid import *

from collections import defaultdict
from functools import cmp_to_key
from typing import Iterable, TextIO, Callable


def do_march(grid: MutableCharacterGrid, location: tuple[int, int]):

    standing_on: str = grid[location]
    velocity: tuple[int, int] = STRIDE_NORTH

    part1 = 0
    while standing_on is not None:
        placed_x = False
        if standing_on == '.':
            grid[location] = 'X'
            part1 += 1
            placed_x = True
        new_y = location[0] + velocity[0]
        new_x = location[1] + velocity[1]
        new_location = new_y, new_x
        if grid[new_location] == '#':
            if placed_x:
                grid[location] = '+'
            velocity = ROTATE_CLOCKWISE[velocity]
        else:
            if placed_x:
                if velocity == STRIDE_NORTH or velocity == STRIDE_SOUTH:
                    grid[location] = '|'
                else:
                    grid[location] = '-'
            elif grid[location] == '-' and (velocity == STRIDE_NORTH or velocity == STRIDE_SOUTH):
                grid[location] = '+'
            elif grid[location] == '|' and not (velocity == STRIDE_NORTH or velocity == STRIDE_SOUTH):
                grid[location] = '+'
            location = new_location
        standing_on = grid[location]

    return part1


def day06() -> None:

    start: float = time.perf_counter()

    part1 = 0

    # load the character grid and remove the guard symbol
    grid, location = MutableCharacterGrid.read_character_grid('input06.txt',  '^')
    assert (location is not None), 'unable to find ^ in character grid'
    grid[location] = '.'

    # march on the grid to get part 1 and draw trails
    part1 = do_march(grid, location)

    print(grid)

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 6 - Guard Gallivant")
    print(f"Part 1: {part1}")
    print("Part 2: TODO")
    print(f"Time Taken: {stop-start:.6f} s")
