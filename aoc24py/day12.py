# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from collections import defaultdict
from typing import Optional

from grid import CharacterGrid


def north(y, x):
    return y - 1, x


def east(y, x):
    return y, x + 1


def south(y, x):
    return y + 1, x


def west(y, x):
    return y, x - 1


def flood(grid: CharacterGrid, y: int, x: int, visited: set[tuple[int, int]], character: str) -> int:

    if (y, x) in visited:
        return 0

    if grid[(y, x)] != character:
        return 0

    visited.add((y, x))

    neighbors = [(y-1, x), (y, x + 1), (y + 1, x), (y, x - 1)]
    neighbors = [(y, x) for (y, x) in neighbors if grid[(y, x)] is not None]

    rv = 1
    for n in neighbors:
        rv += flood(grid, n[0], n[1], visited, character)
    return rv


def signatures(grid: CharacterGrid):
    for y in range(grid.height):
        for x in range(grid.width):
            value = grid[(y, x)]
            signature = set()
            flood(grid, y, x, signature, value)
            yield value, frozenset(signature)


def calc_perimeter2(s: frozenset[tuple[int, int]]):
    print(f"TODO: calculate perimeter2 of {s}")
    return 0


def day12() -> None:

    start: float = time.perf_counter()

    grid = CharacterGrid.read_character_grid("small12.txt")

    # print(grid)

    areas = {}
    perimeters = {}
    values = {}

    for value, signature in signatures(grid):
        if signature not in values:
            values[signature] = value
        if signature not in areas:
            area = len(signature)
            areas[signature] = area
        if signature not in perimeters:
            perimeter = 0
            for y, x in signature:
                if grid[north(y, x)] != value:
                    perimeter += 1
                if grid[east(y, x)] != value:
                    perimeter += 1
                if grid[south(y, x)] != value:
                    perimeter += 1
                if grid[west(y, x)] != value:
                    perimeter += 1
            perimeters[signature] = perimeter

    prices = {l: areas[l] * perimeters[l] for l in areas.keys()}
    perimeters2 = {}
    prices2 = {}

    for s in values.keys():
        perimeters2[s] = calc_perimeter2(s)
        prices2[s] = perimeters2[s] * areas[s]

    part1 = sum(prices.values())
    part2 = sum(prices2.values())

    stop: float = time.perf_counter()

    print(grid)

    print("Advent of Code 2024")
    print("Day 12 - Garden Groups")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
