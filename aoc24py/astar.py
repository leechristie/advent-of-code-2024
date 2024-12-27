# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com

import math
from collections import defaultdict
from typing import Callable, Optional


class BinaryMinHeapNode[E]:

    __slots__ = ['element', 'key', 'index']

    def __init__(self, element: E, key: float, index: int) -> None:
        self.element = element
        self.key = key
        self.index = index

    def __str__(self):
        return f'BinaryMinHeapNode({self.element}, {self.key}, {self.index})'

    def __repr__(self):
        return f'BinaryMinHeapNode({self.element}, {self.key}, {self.index})'


class BinaryMinHeap[E]:

    __slots__ = ['heap', 'lookup']

    def __init__(self):
        heap: list[BinaryMinHeapNode[E]] = []
        lookup: dict[E, BinaryMinHeapNode[E]] = {}
        self.heap = heap
        self.lookup = lookup

    def insert(self, element: E, key: float):
        if element in self.lookup:
            raise ValueError(f'duplicate element {element}')
        self.__append_node(element, key)
        index: int = len(self.heap) - 1
        parent_index: int = (index - 1) // 2
        parent_key: Optional[float] = self.heap[parent_index].key if parent_index >= 0 else None
        while parent_key is not None and key < parent_key:
            self.__swap_nodes(index, parent_index)
            index = parent_index
            parent_index = (index - 1) // 2
            parent_key = self.heap[parent_index].key if parent_index >= 0 else None

    def empty(self):
        return len(self.heap) == 0

    def find_min(self) -> E:
        if not self.heap:
            raise ValueError('no elements in heap to find min')
        return self.heap[0].element

    def delete_min(self) -> None:
        if not  self.heap:
            raise ValueError('no elements in heap to delete min')
        self.pop_min()

    def decrease_key(self, element: E, key: float) -> None:
        if element not in self.lookup:
            self.insert(element, key)
            return
        node: BinaryMinHeapNode[E] = self.lookup[element]
        old_key: float = node.key
        if key >= old_key:
            raise ValueError(f'could not decrease key to a non-lower value for {element}')
        node.key = key
        index: int = node.index
        parent_index: int = (index - 1) // 2
        parent_key: Optional[float] = None if parent_index < 0 else self.heap[parent_index].key
        while parent_key is not None and key < parent_key:
            self.__swap_nodes(index, parent_index)
            index = parent_index
            parent_index = (index - 1) // 2
            parent_key = None if parent_index < 0 else self.heap[parent_index].key

    def pop_min(self) -> E:
        if self.empty():
            raise ValueError('no elements in heap to pop min')
        root_element: E = self.heap[0].element
        if len(self.heap) == 1:
            self.heap.clear()
        else:
            self.__swap_nodes(0, len(self.heap) - 1)
            del self.heap[-1]
            self.__repair_heap(0)
        del self.lookup[root_element]
        return root_element

    def __append_node(self, element: E, key: float) -> None:
        index: int = len(self.heap)
        node: BinaryMinHeapNode[E] = BinaryMinHeapNode(element, key, index)
        self.lookup[element] = node
        self.heap.append(node)

    def __swap_nodes(self, a: int, b: int) -> None:
        node_a: BinaryMinHeapNode[E] = self.heap[a]
        node_b: BinaryMinHeapNode[E] = self.heap[b]
        node_a.index = b
        node_b.index = a
        self.heap[a] = node_b
        self.heap[b] = node_a

    def __repair_heap(self, index: int) -> None:
        left_index: int = 2 * index + 1
        right_index: int = left_index + 1
        key: float = self.heap[index].key
        left_key: Optional[float] = self.heap[left_index].key if left_index < len(self.heap) else None
        right_key: Optional[float] = self.heap[right_index].key if right_index < len(self.heap) else None
        smallest_index: int = index
        smallest_key: float = key
        if left_key is not None and left_key < smallest_key:
            smallest_key = left_key
            smallest_index = left_index
        if right_key is not None and right_key < smallest_key:
            smallest_index = right_index
        if smallest_index != index:
            self.__swap_nodes(index, smallest_index)
            self.__repair_heap(smallest_index)


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
    open_set: BinaryMinHeap[T] = BinaryMinHeap()
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


def reachable[T](start: T,
                 goal: Callable[[T], bool],
                 heuristic: Callable[[T], int],
                 neighbours: Callable[[T], list[tuple[T, int]]]) -> bool:
    open_set: BinaryMinHeap[T] = BinaryMinHeap()
    open_set.insert(start, heuristic(start))
    came_from: dict[T, T] = {}
    g_score: dict[T, float] = defaultdict(lambda: math.inf)
    g_score[start] = 0
    f_score: dict[T, float] = defaultdict(lambda: math.inf)
    f_score[start] = heuristic(start)
    while not open_set.empty():
        current: T = open_set.pop_min()
        if goal(current):
            return True
        for neighbor, cost in neighbours(current):
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                neighbor_f_score = tentative_g_score + heuristic(neighbor)
                f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                open_set.decrease_key(neighbor, neighbor_f_score)
    return False
