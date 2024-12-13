# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from fractions import Fraction
from typing import TextIO, Iterable, cast, Optional


class AugmentedRow2D:

    def __init__(self, x: int | Fraction, y: int | Fraction, augment: int | Fraction) -> None:
        self.x = x
        self.y = y
        self.augment = augment

    def __mul__(self, other: int | Fraction) -> 'AugmentedRow2D':
        return AugmentedRow2D(self.x * other, self.y * other, self.augment * other)

    def __truediv__(self, other: int | Fraction) -> 'AugmentedRow2D':
        return AugmentedRow2D(Fraction(self.x, other), Fraction(self.y, other), Fraction(self.augment, other))

    def __sub__(self, other: 'AugmentedRow2D') -> 'AugmentedRow2D':
        return AugmentedRow2D(self.x - other.x, self.y - other.y, self.augment - other.augment)


class Machine:

    def __init__(self, button_a: tuple[int, int], button_b: tuple[int, int], prizes: tuple[int, int]):
        self.button_a = button_a
        self.button_b = button_b
        self.prizes = prizes

    @staticmethod
    def parse(lines: list[str]) -> 'Machine':
        assert len(lines) == 3
        button_a: tuple[int, int] = cast(tuple[int, int], tuple([int(value.split('+')[1]) for value in lines[0].split(': ')[1].split(', ')]))
        button_b: tuple[int, int] = cast(tuple[int, int], tuple([int(value.split('+')[1]) for value in lines[1].split(': ')[1].split(', ')]))
        prizes: tuple[int, int] = cast(tuple[int, int], tuple([int(value.split('=')[1]) for value in lines[2].split(': ')[1].split(', ')]))
        return Machine(button_a, button_b, prizes)

    @staticmethod
    def parse_all(file: TextIO) -> Iterable['Machine']:
        try:
            while True:
                yield Machine.parse([next(file), next(file), next(file)])
                assert next(file) == '\n'
        except StopIteration:
            return

    def compute_cost(self, error: int=0) -> Optional[int]:
        presses = self.compute_number_of_presses(error=error)
        if presses is None:
            return None
        a, b = presses
        return a * 3 + b

    def compute_number_of_presses(self, error: int=0) -> Optional[tuple[int, int]]:
        row1 = AugmentedRow2D(self.button_a[0], self.button_b[0], self.prizes[0] + error)
        row2 = AugmentedRow2D(self.button_a[1], self.button_b[1], self.prizes[1] + error)
        row1 = row1 / row1.x
        row2 = row2 / row2.x
        row2 = row1 - row2
        row2 = row2 / row2.y
        row2 = row2 * row1.y
        row1 = row1 - row2
        row2 = row2 / row2.y
        assert row1.x == 1 and row1.y == 0
        assert row2.x == 0 and row2.y == 1
        a = row1.augment
        b = row2.augment
        if a == int(a) and b == int(b) and a >= 0 and b >= 0 and (a > 0 or b > 0):
            a = int(a)
            b = int(b)
            return a, b
        return None

    @staticmethod
    def cost(a, b):
        assert type(a) == int and type(b) == int and a>= 0 and b >= 0
        return a * 3 + b


def day13() -> None:

    start: float = time.perf_counter()

    part1 = 0
    part2 = 0

    with open('input13.txt') as file:
        for machine in Machine.parse_all(file):

            needed = machine.compute_cost()
            if needed is not None:
                part1 += needed

            needed = machine.compute_cost(error=10000000000000)
            if needed is not None:
                part2 += needed

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 13 - Claw Contraption")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
