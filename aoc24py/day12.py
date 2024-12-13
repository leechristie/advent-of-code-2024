# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from typing import Optional

from grid import CharacterGrid, STRIDE_NORTH, STRIDE_EAST, STRIDE_SOUTH, STRIDE_WEST


class Grid[T]:

    def __init__(self, height: int, width: int, fill: T) -> None:
        self.height = height
        self.width = width
        self.data = [[fill] * width for _ in range(height)]

    def __getitem__(self, item: tuple[int, int]) -> T:
        return self.data[item[0]][item[1]]

    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        self.data[key[0]][key[1]] = value

    def __str__(self) -> str:
        rv = ''
        for y in range(self.height):
            for x in range(self.width):
                if x != 0:
                    rv += '\t'
                rv += str(self[(y, x)]) if self[(y, x)] is not None else '.'
            rv += '\n'
        return rv


def flood(grid: CharacterGrid, y: int, x: int, visited: set[tuple[int, int]], character: str, grid_to_plot_id: Grid[Optional[int]], plot_id: int) -> int:

    if (y, x) in visited:
        return 0

    if grid[(y, x)] != character:
        return 0

    visited.add((y, x))
    grid_to_plot_id[(y, x)] = plot_id

    neighbors = [(y-1, x), (y, x + 1), (y + 1, x), (y, x - 1)]
    neighbors = [(y, x) for (y, x) in neighbors if grid[(y, x)] is not None]

    rv = 1
    for n in neighbors:
        rv += flood(grid, n[0], n[1], visited, character, grid_to_plot_id, plot_id)
    return rv


def get_oriented_edges(sparse: frozenset[tuple[int, int]], grid: CharacterGrid, stride: tuple[int, int], x_is_primary_axis: bool) -> list[tuple[int, int]]:
    dy, dx = stride
    edges: list[tuple[int, int]] = []
    value: Optional[int] = None
    for y, x in sparse:
        if value is None:
            value = grid[(y, x)]
        neighbour = y + dy, x + dx
        if grid[neighbour] != value:
            if x_is_primary_axis:
                primary, secondary = x, y
            else:
                primary, secondary = y, x
            edges.append((primary, secondary))
    return sorted(edges)


def group_by_primary_axis(edges: list[tuple[int, int]]) -> dict[int, list[int]]:
    rv: dict[int, list[int]] = {}
    for p, s in edges:
        if p not in rv:
            rv[p] = []
        rv[p].append(s)
    return rv


def count_gaps(segments_by_secondary: list[int]) -> int:
    rv = 0
    for i in range(len(segments_by_secondary) - 1):
        j = i + 1
        if segments_by_secondary[j] != segments_by_secondary[i] + 1:
            rv += 1
    return rv


def count_segments(edges: list[tuple[int, int]]) -> int:
    rv: int = 0
    for primary, segments_by_secondary in group_by_primary_axis(edges).items():
        gaps = count_gaps(segments_by_secondary)
        rv += 1 + gaps
    return rv


def day12() -> None:

    start: float = time.perf_counter()

    grid = CharacterGrid.read_character_grid("input12.txt")

    grid_to_plot_id: Grid[Optional[int]] = Grid(grid.height, grid.width, None)

    plot_id_to_sparce_point_set = []
    next_plot_id = 0
    for y in range(grid.height):
        for x in range(grid.width):
            location = y, x
            has_been_visited = grid_to_plot_id[location] is not None
            if not has_been_visited:
                visited: set[tuple[int, int]] = set()
                character = grid[location]
                flood(grid, y, x, visited, character, grid_to_plot_id, next_plot_id)
                next_plot_id += 1
                plot_id_to_sparce_point_set.append(frozenset(visited))

    part1 = 0
    part2 = 0
    for i, sparse in enumerate(plot_id_to_sparce_point_set):
        area = len(sparse)
        north_edges = get_oriented_edges(sparse, grid, STRIDE_NORTH, False)
        east_edges = get_oriented_edges(sparse, grid, STRIDE_EAST, True)
        south_edges = get_oriented_edges(sparse, grid, STRIDE_SOUTH, False)
        west_edges = get_oriented_edges(sparse, grid, STRIDE_WEST, True)
        perimeter = sum(len(edges) for edges in (north_edges, east_edges, south_edges, west_edges))
        part1 += perimeter * area
        north_segment_counts = count_segments(north_edges)
        east_segment_counts = count_segments(east_edges)
        south_segment_counts = count_segments(south_edges)
        west_segment_counts = count_segments(west_edges)
        perimeter2 = sum((north_segment_counts, east_segment_counts, south_segment_counts, west_segment_counts))
        part2 += perimeter2 * area

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 12 - Garden Groups")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
