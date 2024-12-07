# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time

from grid import *


def day04() -> None:

    start: float = time.perf_counter()

    part1 = 0
    part2 = 0

    grid = CharacterGrid.read_character_grid('input04.txt')

    for y in range(grid.height):
        for x in range(grid.width):
            for stride in ALL_STRIDES:
                if grid.characters_stride((y, x), stride, 4) == 'XMAS':
                    part1 += 1
            if grid[(y, x)] == 'A':
                nw_to_se = grid.characters_stride((y-1, x-1), STRIDE_SOUTHEAST, 3)
                ne_to_sw = grid.characters_stride((y-1, x+1), STRIDE_SOUTHWEST, 3)
                if (nw_to_se == 'MAS' or nw_to_se == 'SAM') and (ne_to_sw == 'MAS' or ne_to_sw == 'SAM'):
                    part2 += 1

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 4 - Ceres Search")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
