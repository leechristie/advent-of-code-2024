# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from functools import cache


def load_rocks() -> list[int]:
    with open('input11.txt') as file:
        for line in file:
            line = line.strip()
            return [int(e) for e in line.split()]


@cache
def num_final_rocks(rock_number: int, blinks: int) -> int:

    if blinks == 0:
        return 1

    if rock_number == 0:
        return num_final_rocks(1, blinks - 1)

    else:

        rock_str = str(rock_number)
        length = len(rock_str)
        if length % 2 == 0:
            mid = length // 2
            left, right = int(rock_str[:mid]), int(rock_str[mid:])
            return num_final_rocks(left, blinks - 1) + num_final_rocks(right, blinks - 1)

        else:
            return num_final_rocks(rock_number * 2024, blinks - 1)


def day11() -> None:

    start: float = time.perf_counter()

    part1 = 0
    part2 = 0
    for rock in load_rocks():
        part2 += num_final_rocks(rock, 75)
        part1 += num_final_rocks(rock, 25)

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 11 - Plutonian Pebbles")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
