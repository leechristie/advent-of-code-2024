# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from collections.abc import Iterable
from functools import cache


def problems(filename: str) -> Iterable[tuple[int, list[int]]]:
    with open(filename) as file:
        for line in file:
            line = line.strip()
            total, numbers = line.split(': ')
            total = int(total)
            numbers = [int(n) for n in numbers.split(' ')]
            yield total, numbers


def can_be_true_recursive(target: int, numbers: list[int], first_index: int, cumulative: int) -> bool:

    # check if exceeded the target
    if cumulative > target:
        return False

    # check if reached end of list
    if first_index >= len(numbers):
        return target == cumulative

    # case when the next operation is a multiply
    cumulative_with_multiply = cumulative * numbers[first_index]
    if can_be_true_recursive(target, numbers, first_index + 1, cumulative_with_multiply):
        return True

    # case when the next operation is an add
    cumulative_with_add = cumulative + numbers[first_index]
    return can_be_true_recursive(target, numbers, first_index + 1, cumulative_with_add)


def can_be_true(target: int, numbers: list[int]) -> bool:
    return can_be_true_recursive(target, numbers, first_index=1, cumulative=numbers[0])


def can_be_true_with_concat_recursive(target: int, numbers: list[int], first_index: int, cumulative: int) -> bool:

    # check if exceeded the target
    if cumulative > target:
        return False

    # check if reached end of list
    if first_index >= len(numbers):
        return target == cumulative

    # case when the next operation is a multiply
    if can_be_true_with_concat_recursive(target, numbers, first_index + 1, cumulative * numbers[first_index]):
        return True

    # case when the next operation is an add
    if can_be_true_with_concat_recursive(target, numbers, first_index + 1, cumulative + numbers[first_index]):
        return True

    # case when the next operation is a concat
    temp = numbers[first_index]
    while temp > 0:
        temp //= 10
        cumulative *= 10
    return can_be_true_with_concat_recursive(target, numbers, first_index + 1, cumulative + numbers[first_index])


def can_be_true_with_concat(target: int, numbers: list[int]) -> bool:
    return can_be_true_with_concat_recursive(target, numbers, first_index=1, cumulative=numbers[0])


def day07() -> None:

    start: float = time.perf_counter()

    part1 = 0
    part2 = 0
    for total, numbers in problems('input07.txt'):
        if can_be_true(total, numbers):
            part1 += total
            part2 += total
        else:
            if can_be_true_with_concat(total, numbers):
                part2 += total

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 7 - Bridge Repair")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
