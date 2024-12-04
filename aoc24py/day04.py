# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from typing import Optional


class CharacterGrid:

    __slots__ = ['data', 'width', 'height']

    def __init__(self, data: list[str]) -> None:
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

    def __getitem__(self, item: tuple[int, int]) -> Optional[str]:
        y, x = item
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.data[y][x]
        return None

    @staticmethod
    def read_character_grid(filename: str) -> 'CharacterGrid':
        lines = []
        with open(filename) as file:
            for line in file:
                line = line.strip()
                lines.append(line)
        return CharacterGrid(lines)

    def __str__(self) -> str:
        rv: str = ''
        for y in range(self.height):
            for x in range(self.width):
                rv += self[(y, x)]
            rv += '\n'
        return rv

    def characters_stride(self, origin: tuple[int, int], stride: tuple[int, int], length: int) -> str:
        rv = ''
        item = origin
        for i in range(length):
            if self[item]:
                rv += self[item]
            item = (item[0] + stride[0], item[1] + stride[1])
        return rv


#                    y   x
STRIDE_NORTH     = (-1,  0)
STRIDE_NORTHEAST = (-1,  1)
STRIDE_EAST      = ( 0,  1)
STRIDE_SOUTHEAST = ( 1,  1)
STRIDE_SOUTH     = ( 1,  0)
STRIDE_SOUTHWEST = ( 1, -1)
STRIDE_WEST      = ( 0, -1)
STRIDE_NORTHWEST = (-1, -1)


ALL_STRIDES = [STRIDE_NORTH, STRIDE_NORTHEAST, STRIDE_EAST, STRIDE_SOUTHEAST,
               STRIDE_SOUTH, STRIDE_SOUTHWEST, STRIDE_WEST, STRIDE_NORTHWEST]


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
