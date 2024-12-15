# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from collections.abc import Generator
from typing import Optional

from grid import MutableCharacterGrid


def direction_arrows(directions_string: str) -> Generator[[None], tuple[int, int]]:
    for char in directions_string:
        if char == '^':
            yield -1, 0
        elif char == '>':
            yield 0, 1
        elif char == 'v':
            yield 1, 0
        elif char == '<':
            yield 0, -1


def buddy(grid: MutableCharacterGrid, y: int, x: int) -> tuple[int, int]:
    assert grid[(y, x)] == '[' or grid[(y, x)] == ']'
    if grid[(y, x)] == '[':
        return y, x + 1
    return y, x - 1


def move(grid: MutableCharacterGrid, y: int, x: int, dy: int, dx: int, buddy_push:bool=False) -> None:
    character: Optional[str] = grid[(y, x)]
    assert character is not None
    assert character != '#'
    if character == '.':
        return
    if dx == 1:  # right (east)
        assert dy == 0
        assert (character == '[' or character == ']'), f'tried to push {character}'
        move(grid, y, x + 1, dy, dx)
        assert grid[(y + dy, x + dx)] == '.'
        grid[(y + dy, x + dx)] = character
        grid[(y, x)] = '.'
        #print(f'actually moved a {character} right')
        return
    if dx == -1:  # left (west)
        assert dy == 0
        assert (character == '[' or character == ']'), f'tried to push {character}'
        move(grid, y, x - 1, dy, dx)
        assert grid[(y + dy, x + dx)] == '.'
        grid[(y + dy, x + dx)] = character
        grid[(y, x)] = '.'
        #print(f'actually moved a {character} left')
        return
    if dy == 1:  # down (south)
        assert dx == 0
        assert (character == '[' or character == ']'), f'tried to push {character}'
        move(grid, y + 1, x, dy, dx)
        if not buddy_push:  # not already moving as a result of a buddy push
            buddy_y, buddy_x = buddy(grid, y, x)
            move(grid, buddy_y, buddy_x, dy, dx, buddy_push=True)
        grid[(y + dy, x + dx)] = character
        grid[(y, x)] = '.'
        return
    if dy == -1:  # up (north)
        assert dx == 0
        assert (character == '[' or character == ']'), f'tried to push {character}'
        move(grid, y - 1, x, dy, dx)
        if not buddy_push:  # not already moving as a result of a buddy push
            buddy_y, buddy_x = buddy(grid, y, x)
            move(grid, buddy_y, buddy_x, dy, dx, buddy_push=True)
        grid[(y + dy, x + dx)] = character
        grid[(y, x)] = '.'
        return
    assert False, 'unknown option in push'


def stops_movement(grid: MutableCharacterGrid, y: int, x: int, dy: int, dx: int, buddy_push=False) -> bool:
    character: Optional[str] = grid[(y, x)]
    if character == '[':
        assert (grid[(y, x + 1)] == ']'), "[ lost it's ]"
    if character == ']':
        assert (grid[(y, x - 1)] == '['), "] lost it's ["
    #print(f'checking if can push {character} at {y, x} in direction {dy, dx} ({recursive=}) ...')
    assert character is not None
    if character == '#':
        return True
    if character == '.':
        return False
    if dx == 1:  # right (east)
        assert dy == 0
        assert (character == '[' or character == ']'), f'tried to think about pushing {character}'
        return stops_movement(grid, y, x + 1, dy, dx)
    elif dx == -1:  # left (west)
        assert dy == 0
        assert (character == '[' or character == ']'), f'tried to think about pushing {character}'
        return stops_movement(grid, y, x - 1, dy, dx)
    elif dy == 1:  # down (south)
        assert dx == 0
        assert (character == '[' or character == ']'), f'tried to think about pushing {character}'
        if not buddy_push:  # not already moving as a result of a buddy push
            buddy_y, buddy_x = buddy(grid, y, x)
            if stops_movement(grid, buddy_y, buddy_x, dy, dx, buddy_push=True):
                return True
        return stops_movement(grid, y + 1, x, dy, dx)
    elif dy == -1:  # down (north)
        assert dx == 0
        assert (character == '[' or character == ']'), f'tried to think about pushing {character}'
        if not buddy_push:  # not already moving as a result of a buddy push
            buddy_y, buddy_x = buddy(grid, y, x)
            if stops_movement(grid, buddy_y, buddy_x, dy, dx, buddy_push=True):
                return True
        return stops_movement(grid, y - 1, x, dy, dx)
    return False


def day15() -> None:

    start: float = time.perf_counter()

    ##########
    # Part 1 #
    ##########

    grid, (y, x), footer = MutableCharacterGrid.read_character_grid_with_footer('input15.txt', '@')
    grid[(y, x)] = '.'

    for dy, dx in direction_arrows(footer):
        if grid.push(y, x, dy, dx, 'O', '#'):
            y += dy
            x += dx

    part1 = 0
    for y in range(grid.height):
        for x in range(grid.width):
            good_position = y * 100 + x
            if grid[(y, x)] == 'O':
                part1 += good_position

    ##########
    # Part 2 #
    ##########

    translation = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
    grid, (y, x), footer = MutableCharacterGrid.read_character_grid_with_footer('input15.txt', '@', translation)
    loc = y, x
    grid[loc] = '.'

    for dy, dx in direction_arrows(footer):
        if not stops_movement(grid, y + dy, x + dx, dy, dx):
            move(grid, y + dy, x + dx, dy, dx)
            y += dy
            x += dx

    part2 = 0
    for y in range(grid.height):
        for x in range(grid.width):
            good_position = y * 100 + x
            if grid[(y, x)] == '[':
                part2 += good_position

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 15 - Warehouse Woes")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
