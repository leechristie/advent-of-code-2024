# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
import re


def get_file() -> str:
    all_lines = ''
    with open('input03.txt') as file:
        for line in file:
            all_lines += line
    return all_lines


def day03() -> None:

    start: float = time.perf_counter()

    part1: int = 0
    part2: int = 0

    all_lines = get_file()
    pattern = re.compile(r"mul\((\d\d?\d?),(\d\d?\d?)\)|do\(\)|don't\(\)")
    enabled = True
    for match in re.finditer(pattern, all_lines):
        match_string = all_lines[match.start():match.end()]
        if match_string == 'do()':
            enabled = True
        elif match_string == "don't()":
            enabled = False
        else:
            first, second = match.groups()
            value = int(first) * int(second)
            part1 += value
            if enabled:
                part2 += value


    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 3 - Mull It Over")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
