# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from typing import Optional
from grid import CharacterGrid


def evaluate(grid: CharacterGrid, location: tuple[int, int], ordinal: int) -> tuple[int, set[tuple[int, int]]]:

    # wrong number
    here: Optional[str] = grid[location]
    if here is None or ord(here) != ordinal:
        return 0, set()

    # found goal
    if ordinal == ord('9'):
        return 1, {location}

    # check neighbours
    y, x = location
    trail_count = 0
    trail_ends = set()
    for n in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]:
        score, ends = evaluate(grid, n, ordinal + 1)
        trail_count += score
        trail_ends.update(ends)

    # return all number of trails and reachable trail ends
    return trail_count, trail_ends


def day10() -> None:

    start: float = time.perf_counter()

    part1 = 0
    part2 = 0

    grid = CharacterGrid.read_character_grid("input10.txt")

    for y in range(grid.height):
        for x in range(grid.width):
            location = y, x
            value = grid[location]
            if value == '0':
                count, ends = evaluate(grid, location, ord(value))
                part1 += len(ends)  # number of reachable ends
                part2 += count      # count of unique trails

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 10 - Hoof It")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
