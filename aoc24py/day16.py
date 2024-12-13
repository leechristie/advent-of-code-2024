# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com

import math
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Optional

from grid import MutableCharacterGrid

sys.setrecursionlimit(15000)

@dataclass(eq=True, frozen=True)
class Facing:
    dy: int
    dx: int

    def __len__(self):
        assert self.dx ** 2 + self.dy ** 2 == 1
        return 1

    def dot(self, other: 'Facing') -> int:
        return self.dx * other.dx + self.dy * other.dy

    def inner_angle(self, other: 'Facing') -> int:
        assert len(self) == 1 and len(other) == 1
        cosine = self.dot(other)
        if cosine == 0:
            return 90
        if cosine == -1:
            return 180
        assert cosine == 1
        return 0

    def clockwise90(self) -> 'Facing':
        return Facing(self.dx, -self.dy)

    def counterclockwise90(self) -> 'Facing':
        return Facing(-self.dx, self.dy)


@dataclass(eq=True, frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, d: Facing) -> 'Point':
        return Point(self.y + d.dy, self.x + d.dx)

    def __sub__(self, rhs: 'Point') -> Facing:
        dy = self.y - rhs.y
        dx = self.x - rhs.x
        return Facing(dy, dx)

    def distance(self, other: 'Point') -> int:
        return abs(other.y - self.y) + abs(other.x) - self.x


@dataclass(eq=True, frozen=True)
class State:
    point: Point
    facing: Facing


# TODO: make MinHeap efficient
class MinHeap[T]:

    __slots__ = ['dumb_dict']

    def __init__(self):
        dumb_dict: dict[T, int] = {}
        self.dumb_dict = dumb_dict

    def insert(self, item: T, key: int) -> None:
        assert (item not in self.dumb_dict), 'item already in heap, cannot insert'
        self.dumb_dict[item] = key

    def empty(self) -> bool:
        return not self.dumb_dict

    def find_min(self) -> T:
        rv: Optional[tuple[T, int]] = None
        for item, key in self.dumb_dict.items():
            if rv is None or rv[1] > key:
                rv = item, key
        if rv is None:
            raise ValueError('no items in heap')
        return rv[0]

    def delete_min(self) -> None:
        del self.dumb_dict[self.find_min()]

    def decrease_key(self, item, key) -> None:
        if item in self.dumb_dict:
            assert self.dumb_dict[item] >= key, 'cannot decrease key, already smaller'
        self.dumb_dict[item] = key

    def pop_min(self) -> T:
        rv: T = self.find_min()
        self.delete_min()
        return rv


def compute_path_cost[T](path: list[T],
                         cost: Callable[[T, T], int]) -> int:
    rv: int = 0
    for i in range(len(path) - 1):
        j = i + 1
        rv += cost(path[i], path[j])
    return rv


def num_turns[T](path: list[T], is_turn: Callable[[T, T], bool]) -> int:
    rv: int = 0
    for i in range(len(path) - 1):
        j = i + 1
        rv += 1 if is_turn(path[i], path[j]) else 0
    return rv


def reconstruct_path[T](came_from: dict[T, T],
                        current: T) -> list[T]:
    total_path: list[T] = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]


def a_star[T](start: T,
              goal: Callable[[T], bool],
              heuristic: Callable[[T], int],
              neighbours: Callable[[T], list[tuple[T, int]]]) -> Optional[list[T]]:
    open_set: MinHeap[T] = MinHeap()
    open_set.insert(start, heuristic(start))
    came_from: dict[T, T] = {}
    g_score: dict[T, float] = defaultdict(lambda: math.inf)
    g_score[start] = 0
    f_score: dict[T, float] = defaultdict(lambda: math.inf)
    f_score[start] = heuristic(start)
    while not open_set.empty():
        current: T = open_set.pop_min()
        if goal(current):
            return reconstruct_path(came_from, current)
        for neighbor, cost in neighbours(current):
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                neighbor_f_score = tentative_g_score + heuristic(neighbor)
                f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                open_set.decrease_key(neighbor, neighbor_f_score)
    return None


def find_start_and_end(grid: MutableCharacterGrid,
                       dy: int,
                       dx: int) -> tuple[State, Point]:
    sy, sx = grid.find_first('S')
    ey, ex = grid.find_first('E')
    grid[(sy, sx)] = '.'
    grid[(ey, ex)] = '.'
    sp = Point(sy, sx)
    sf = Facing(dy, dx)
    ss = State(sp, sf)
    ep = Point(ey, ex)
    return ss, ep


DIRECTIONS = Facing(-1, 0), Facing(0, 1), Facing(1, 0), Facing(0, -1)


def compute_neighbor_list(grid: MutableCharacterGrid,
                          current: State,
                          cost: Callable[[State, State], int]) -> list[tuple[State, int]]:
    rv: list[tuple[State, int]] = []
    for facing in DIRECTIONS:
        if current.facing.inner_angle(facing) in [0, 90]:
            neighbor = State(current.point + facing, facing)
            if grid[(neighbor.point.y, neighbor.point.x)] == '.':
                rv.append((neighbor, cost(current, neighbor)))
    return rv


def compute_move_cost(from_state: State,
                      to_state: State,
                      move: int,
                      turn: int) -> int:
    assert to_state.point - from_state.point in DIRECTIONS
    rv = move
    if from_state.facing != to_state.facing:
        assert from_state.facing.inner_angle(to_state.facing) in [0, 90]
        rv += turn
    return rv


def facing_symbol(facing: Facing) -> str:
    if (facing.dy, facing.dx) == (-1, 0):
        return '^'
    if (facing.dy, facing.dx) == (0, 1):
        return '>'
    if (facing.dy, facing.dx) == (1, 0):
        return 'v'
    if (facing.dy, facing.dx) == (0, -1):
        return '<'
    raise ValueError(f'unknown symbol for facing {facing}')


def symbol_at(grid: MutableCharacterGrid, path: list[State], y: int, x: int) -> str:
    for state in path:
        if state.point.y == y and state.point.x == x:
            return facing_symbol(state.facing)
    return grid[(y, x)]


def print_path(grid: MutableCharacterGrid, path: list[State]) -> None:
    for y in range(grid.height):
        for x in range(grid.width):
            print(symbol_at(grid, path, y, x), end='')
        print()


def move_is_turn(form_state: State, to_state: State) -> bool:
    return form_state.facing != to_state.facing


def is_dead_end(grid: MutableCharacterGrid, y: int, x: int) -> bool:
    if grid[(y, x)] != '.':
        return False
    walls = 0
    for neighbour in ((y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)):
        if grid[neighbour] == '#' or grid[neighbour] == '?':
            walls += 1
    return walls > 2


def fill_dead_end(grid: MutableCharacterGrid, y: int, x: int) -> None:
    if not is_dead_end(grid, y, x):
        return
    grid[(y, x)] = '#'
    for ny, nx in ((y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)):
        fill_dead_end(grid, ny, nx)


def fill_dead_ends(grid: MutableCharacterGrid) -> None:
    for y in range(grid.height):
        for x in range(grid.width):
            fill_dead_end(grid, y, x)


def is_vertex(grid: MutableCharacterGrid, y: int, x: int) -> bool:
    if grid[(y, x)] == '#':
        return False
    if grid[(y, x)] == 'S' or grid[(y, x)] == 'E':
        return True
    ways_out = 0
    for ny, nx in ((y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)):
        if grid[(ny, nx)] != '#':
            ways_out += 1
    assert (ways_out != 1 and ways_out != 0), f'at {y, x}, found a point with {ways_out} ways out that is not S or E'
    return ways_out >= 3


def find_vertices(grid: MutableCharacterGrid) -> list[Point]:
    rv: list[Point] = []
    for y in range(grid.height):
        for x in range(grid.width):
            if is_vertex(grid, y, x):
                rv.append(Point(y, x))
    return rv


START_DY, START_DX = 0, 1
MOVE_COST, TURN_COST = 1, 1000


def print_with_overlay(grid: MutableCharacterGrid, vertices: list[Point]) -> None:
    symbols = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    count = 0
    for y in range(grid.height):
        for x in range(grid.width):
            if Point(y, x) not in vertices:
                print(grid[(y, x)], end='')
            else:
                if count >= len(symbols):
                    print('?', end='')
                else:
                    print(symbols[count], end='')
                    count += 1
        print()


def news(facing: Facing) -> str:
    if facing == Facing(-1, 0):
        return 'North'
    if facing == Facing(0, 1):
        return 'East'
    if facing == Facing(1, 0):
        return 'South'
    if facing == Facing(0, -1):
        return 'West'
    raise AssertionError('unknown facing in news')


def can_go(grid: MutableCharacterGrid, vertex: Point, facing: Facing) -> bool:
    return grid[(vertex.y + facing.dy, vertex.x + facing.dx)] == '.'


def one_of[T](a: Optional[T], b: Optional[T]) -> T:
    if a is not None:
        return a
    assert b is not None
    return b


def to_next_vertex(grid: MutableCharacterGrid, point: Point, facing: Facing, origin: Optional[Point], vertex_lookup: dict[Point, int], called_as:str='top level call') -> Optional[tuple[int, int, int]]:

    # if origin == Point(3, 3):
    #     print(f'    to_next_vertex called on point {point} facing {news(facing)}, called as {called_as}')

    if grid[(point.y, point.x)] == '#':
        return None

    # found a point, stop
    if point != origin and point in vertex_lookup:
        return 0, 0, vertex_lookup[point]

    # check if we need to turn
    forward = point + facing
    if grid[(forward.y, forward.x)] == '#':

        facing_counterclockwise90 = facing.counterclockwise90()
        move_counterclockwise90 = point + facing_counterclockwise90
        rv_counterclockwise90: Optional[tuple[int, int, int]] = to_next_vertex(grid, move_counterclockwise90, facing_counterclockwise90, None, vertex_lookup, 'counter clockwise 90 turn')

        facing_clockwise90 = facing.clockwise90()
        move_clockwise90 = point + facing_clockwise90
        rv_clockwise90: Optional[tuple[int, int, int]] = to_next_vertex(grid, move_clockwise90, facing_clockwise90, None, vertex_lookup, 'clockwise 90 turn')

        if rv_counterclockwise90 is None and rv_clockwise90 is None:
            return None
        assert (rv_counterclockwise90 is None or rv_clockwise90 is None), 'got non None result for both rv_counterclockwise90 and rv_clockwise90'
        num_steps, num_turns, destination_id = one_of(rv_counterclockwise90, rv_clockwise90)
        return num_steps + 1, num_turns + 1, destination_id

    # if we don't need to turn
    move_forward = point + facing
    rv_forward: Optional[tuple[int, int, int]] = to_next_vertex(grid, move_forward, facing, None, vertex_lookup, 'forward step')
    if rv_forward is None:
        return None
    num_steps, num_turns, destination_id = rv_forward
    return num_steps + 1, num_turns, destination_id


def invert_list_to_dict[T](items: list[T]) -> dict[T, int]:
    rv: dict[T, int] = {}
    for index, item in enumerate(items):
        rv[item] = index
    return rv


def day16() -> None:

    start: float = time.perf_counter()

    part1 = None
    part2 = 0

    # load the character grid from the input file
    # grid, _ = MutableCharacterGrid.read_character_grid('tiny16.txt', '\0')  # 4012
    # grid, _ = MutableCharacterGrid.read_character_grid('three16.txt', '\0')  # 25086
    # grid, _ = MutableCharacterGrid.read_character_grid('test16.txt', '\0')  # 7036
    # grid, _ = MutableCharacterGrid.read_character_grid('second16.txt', '\0')  # 11048
    grid, _ = MutableCharacterGrid.read_character_grid('input16.txt', '\0')  # 94444
    # print(grid)

    # fill in the areas that are an unbranching path leading to a dead end
    fill_dead_ends(grid)
    # print(grid)

    # find the vertices
    vertices = find_vertices(grid)
    vertex_lookup = invert_list_to_dict(vertices)
    # print_with_overlay(grid, vertices)

    # find the start and end, and remove the placeholder symbols from the grid
    start_state, goal_point = find_start_and_end(grid, START_DY, START_DX)

    # search for the shortest path the start to the goal (Part 1 solution)
    cost_function = lambda from_state, to_state: compute_move_cost(from_state, to_state, MOVE_COST, TURN_COST)
    path: Optional[list[State]] = a_star(
        start_state,
        lambda state: state.point == goal_point,
        lambda state: state.point.distance(goal_point) * MOVE_COST,
        lambda state: compute_neighbor_list(grid, state, cost_function))
    if path:
        path_cost = compute_path_cost(path, cost_function)
        part1 = path_cost

    ############
    ## PART 2 ##
    ############

    print('vertices :', len(vertices))

    reduced_graph_neighbours: dict[tuple[Point, Facing], tuple[Point, int]] = {}

    # reduce the graph to a vertices and pre-compute the single next vertex reachable by moving in each of 4 directions with cost
    # symbols = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, vertex in enumerate(vertices):
        # symbol = symbols[i] if i < len(symbols) else '?'
        for facing in DIRECTIONS:
            if can_go(grid, vertex, facing):
                num_steps, num_turns, destination = to_next_vertex(grid, vertex, facing, vertex, vertex_lookup)
                if destination != vertex_lookup[vertex]:
                    cost = num_steps + MOVE_COST + num_turns * TURN_COST
                    # print(f'can go {news(facing)} from vertex {vertex}', end='')
                    # if symbol == '?':
                    #     print(f' ({i}) ', end='')
                    # else:
                    #     print(f' ({symbol}) ', end='')
                    # print(f'({num_steps=}, {num_turns=}, {destination=}, {cost=})')
                    assert (vertex, facing) not in reduced_graph_neighbours
                    reduced_graph_neighbours[(vertex, facing)] = destination, cost

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 16 - Reindeer Maze")
    print(f"Part 1: {part1}")
    assert (part1 in {4012, 7036, 25086, 11048, 94444}), f'{part1 = }, expected one of 4012, 7036, 25086, 11048, 94444'
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
