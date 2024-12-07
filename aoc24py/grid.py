# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


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


class MutableCharacterGrid():

    __slots__ = ['data', 'width', 'height']

    def __init__(self, data: list[list[str]]) -> None:
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

    def __setitem__(self, key: tuple[int, int], value: str) -> None:
        y, x = key
        assert len(value) == 1
        if not 0 <= y < self.height or not 0 <= x < self.width:
            print(f'warning dropped write at ({y}, {x})')
            return
        self.data[y][x] = value

    def __getitem__(self, item: tuple[int, int]) -> Optional[str]:
        y, x = item
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.data[y][x]
        return None

    @staticmethod
    def read_character_grid(filename: str, locator: str) -> tuple['MutableCharacterGrid', tuple[int, int]]:
        lines = []
        location = None
        with open(filename) as file:
            for y, line in enumerate(file):
                line = list(line.strip())
                for x, c in enumerate(line):
                    if c == locator:
                        location = (y, x)
                lines.append(line)
        return MutableCharacterGrid(lines), location

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

ROTATE_CLOCKWISE = {
    STRIDE_NORTH: STRIDE_EAST,
    STRIDE_EAST: STRIDE_SOUTH,
    STRIDE_SOUTH: STRIDE_WEST,
    STRIDE_WEST: STRIDE_NORTH
}

ROTATE_COUNTERCLOCKWISE = {
    STRIDE_EAST: STRIDE_NORTH,
    STRIDE_SOUTH: STRIDE_EAST,
    STRIDE_WEST: STRIDE_SOUTH,
    STRIDE_NORTH: STRIDE_WEST
}
