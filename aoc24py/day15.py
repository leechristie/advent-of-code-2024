# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from collections.abc import Generator

from grid import MutableCharacterGrid


def direction_arrows(directions_string: str) -> Generator[[None], tuple[int, int]]:
    for char in directions_string:
        if char == '^':
            yield -1, 0
        elif char == '>':
            yield 0, 1
        elif char == 'v':
            yield 1, 0
        elif char == '<':
            yield 0, -1


def day15() -> None:

    start: float = time.perf_counter()

    ##########
    # Part 1 #
    ##########

    grid, (y, x), footer = MutableCharacterGrid.read_character_grid_with_footer('input15.txt', '@')

    for dy, dx in direction_arrows(footer):
        if grid.push(y, x, dy, dx, 'O', '#'):
            y += dy
            x += dx

    part1 = 0
    for y in range(grid.height):
        for x in range(grid.width):
            good_position = y * 100 + x
            if grid[(y, x)] == 'O':
                part1 += good_position

    ##########
    # Part 2 #
    ##########

    part2 = 0

    translation = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
    grid, (y, x), footer = MutableCharacterGrid.read_character_grid_with_footer('small15.txt', '@', translation)

    print('before:')
    grid.print_with_symbol(y, x, '@')
    print(y, x)
    print()

    

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 15 - Warehouse Woes")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
