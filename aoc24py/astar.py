# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com

import math
from collections import defaultdict
from typing import Callable, Optional


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
