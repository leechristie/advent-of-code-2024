# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from collections import defaultdict
from functools import cmp_to_key
from typing import Iterable, TextIO, Callable


def read_header(file: TextIO) -> Iterable[tuple[int, int]]:
    for line in file:
        line = line.strip()
        if not line:
            break
        assert '|' in line
        a, b = line.split('|')
        a = int(a)
        b = int(b)
        yield a, b


def read_body(file: TextIO) -> Iterable[list[int]]:
    for line in file:
        line = line.strip()
        if not line:
            break
        assert ',' in line
        items = [int(i) for i in line.split(',')]
        assert len(items) % 2 == 1
        yield items


def correctly_ordered(items: list[int], orders: dict[int, list[int]]) -> bool:
    for i in range(0, len(items)-1):
        a = items[i]
        j = i + 1
        b = items[j]
        if a in orders[b]:
            return False
    return True


def middle_item(items: list[int]) -> int:
    assert len(items) % 2 == 1
    return items[len(items) // 2]


def make_cmp(orders: dict[int, list[int]]) -> Callable[[int, int], int]:
    def cmp(a: int, b: int):
        if a in orders[b]:
            return 1
        elif b in orders[a]:
            return -1
        else:
            assert a == b
            return 0
    return cmp


def sort(items: list[int], cmp: Callable[[int, int], int]) -> bool:
    items.sort(key=cmp_to_key(cmp))


def day05() -> None:

    start: float = time.perf_counter()

    part1 = 0
    part2 = 0

    with open('input05.txt') as file:
        orders: dict[int, list[int]] = defaultdict(list)
        for a, b in read_header(file):
            orders[a].append(b)
        for items in read_body(file):
            if correctly_ordered(items, orders):
                part1 += middle_item(items)
            else:
                cmp = make_cmp(orders)
                sort(items, cmp)
                part2 += middle_item(items)


    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 5 - Print Queue")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
