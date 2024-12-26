# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from typing import Generator

from astar import *
from grid import MutableCharacterGrid
from twodee import *

def read_input(filename: str, limit: Optional[int]=None) -> Generator[Point]:
    assert limit is None or (type(limit) == int and limit > 0)
    count = 0
    with open(filename) as file:
        for line in file:
            line = line.strip()
            x, y = line.split(',')
            x = int(x)
            y = int(y)
            assert 0 <= x <= 70
            assert 0 <= y <= 70
            yield Point(y, x)
            count += 1
            if limit is not None and count >= limit:
                break

# HEIGHT = 7
# WIDTH = 7
# FILENAME = 'test18.txt'
# LIMIT = 12

HEIGHT = 71
WIDTH = 71
FILENAME = 'input18.txt'
LIMIT = 1024


def neighbours_on(grid: MutableCharacterGrid) -> Callable[[Point], list[tuple[Point, int]]]:
    def neighbours(p: Point) -> list[tuple[Point, int]]:
        rv: list[tuple[Point, int]] = []
        y = p.y
        x = p.x
        for neighbour in ((y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)):
            if grid[neighbour] == '.':
                rv.append((Point(neighbour[0], neighbour[1]), 1))
        return rv
    return neighbours


def day18() -> None:

    start: float = time.perf_counter()

    end_point: Point = Point(HEIGHT - 1, WIDTH - 1)

    grid = MutableCharacterGrid.blank(HEIGHT, WIDTH, '.')

    for point in read_input(FILENAME, limit=LIMIT):
        grid[(point.y, point.x)] = '#'

    start_point: Point = Point(0, 0)  # T
    goal: Callable[[Point], bool] = lambda p: p == end_point
    heuristic: Callable[[Point], int] = lambda p: end_point.distance(p)

    path = a_star(start_point, goal, heuristic, neighbours_on(grid))
    part1: int = len(path) - 1

    all_failed_bytes = list(read_input(FILENAME))

    part2: str = ''
    for index, failed_byte in enumerate(all_failed_bytes):
        if index < LIMIT:
            assert grid[(failed_byte.y, failed_byte.x)] == '#'
        else:
            assert grid[(failed_byte.y, failed_byte.x)] == '.'
            grid[(failed_byte.y, failed_byte.x)] = '#'
            path = a_star(start_point, goal, heuristic, neighbours_on(grid))
            if path is None:
                part2 = f'{failed_byte.x},{failed_byte.y}'
                break

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 18 - RAM Run")
    print(f"Part 1: {part1}")
    assert part1 in (22, 360)
    print(f"Part 2: {part2}")
    assert part2 in ('6,1', '58,62')
    print(f"Time Taken: {stop-start:.6f} s")
