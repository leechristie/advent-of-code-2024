# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com
import re
import time
from functools import cache
from itertools import count


def read_input(filename: str) -> tuple[list[str], list[str]]:
    targets: list[str] = []
    with open(filename) as file:
        materials = next(file).strip().split(', ')
        assert next(file).strip() == ''
        for target in file:
            target = target.strip()
            targets.append(target)
    return materials, targets


def symbol_set(materials: list[str]) -> set[str]:
    rv: set[str] = set()
    for material in materials:
        for symbol in material:
            rv.add(symbol)
    return rv


def encode(target: str, symbols: dict[str, int]) -> list[int]:
    rv: list[int] = []
    for character in target:
        rv.append(symbols[character])
    return rv


def fits_here(next_match: list[int], encoded_target: list[int], lower: int) -> bool:
    for index, symbol in enumerate(next_match):
        offset_index = index + lower
        if offset_index >= len(encoded_target):
            return False
        if symbol != encoded_target[offset_index]:
            return False
    return True


def ways_of_matching(encoded_target: list[int], encoded_materials: list[list[int]]) -> int:

    @cache
    def ways_of_tail_matching(lower: int) -> int:

        if lower == len(encoded_target):
            return 1

        found_match_next_tails: list[int] = []
        for next_match in encoded_materials:
            if fits_here(next_match, encoded_target, lower):
                found_match_next_tails.append(lower + len(next_match))

        if not found_match_next_tails:
            return 0

        rv = 0
        for next_lower in found_match_next_tails:
            rv += ways_of_tail_matching(next_lower)
        return rv

    return ways_of_tail_matching(0)


def day19() -> None:

    start: float = time.perf_counter()

    materials, targets = read_input('input19.txt')

    symbols = {s: i for s, i in zip(sorted(symbol_set(materials)), count())}

    encoded_materials: list[list[int]] = [encode(material, symbols) for material in materials]

    part1: int = 0
    part2: int = 0
    for target in targets:
        encoded_target: list[int] = encode(target, symbols)
        number_of_ways = ways_of_matching(encoded_target, encoded_materials)
        if number_of_ways:
            part1 += 1
        part2 += number_of_ways

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 19 - Linen Layout")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
