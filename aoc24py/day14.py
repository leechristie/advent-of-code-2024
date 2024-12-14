# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time

from collections import Counter
from collections.abc import Generator


class Robot:

    def __init__(self, y: int, x: int, dy: int, dx: int) -> None:
        self.y = y
        self.x = x
        self.dy = dy
        self.dx = dx

    @staticmethod
    def parse(line: str) -> 'Robot':
        line = line.strip()
        position, velocity = line.split(' ')
        y, x = tuple(reversed([int(e) for e in position.removeprefix('p=').split(',')]))
        dy, dx = tuple(reversed([int(e) for e in velocity.removeprefix('v=').split(',')]))
        return Robot(y, x, dy, dx)

    @staticmethod
    def print_grid(robots: list['Robot'], height: int, width: int) -> None:
        for y in range(height):
            for x in range(width):
                num_bots = 0
                for bot in robots:
                    if bot.is_at(y, x):
                        num_bots += 1
                print(num_bots if num_bots else '.', end='')
            print()
        print()

    def is_at(self, y: int, x: int) -> bool:
        return self.y == y and self.x == x

    def step(self, height: int, width: int) -> None:
        self.y += self.dy
        self.x += self.dx
        while self.y < 0:
            self.y += height
        while self.x < 0:
            self.x += width
        while self.y >= height:
            self.y -= height
        while self.x >= width:
            self.x -= width

    @staticmethod
    def quadrent(height: int, width: int, y: int, x: int) -> int:
        if y < height // 2:
            if x < width // 2:
                return 1
            if x > width // 2:
                return 2
        if y > height // 2:
            if x < width // 2:
                return 3
            if x > width // 2:
                return 4
        return 0


def do_part1_section_counts(robots: list[Robot], height: int, width: int) -> int:
    counter = Counter()
    for y in range(height):
        for x in range(width):
            quad = Robot.quadrent(height, width, y, x)
            for r in robots:
                if r.is_at(y, x):
                    counter[quad] += 1
    rv = 1
    for k, v in counter.items():
        if k != 0:
            rv *= v
    return rv


def calc_variation(values: list[float]) -> float:
    mean = sum(values) / len(values)
    return sum((x - mean) ** 2 for x in values) / len(values)


def find_variance(robots: list[Robot]) -> tuple[float, float]:
    y_values = []
    x_values = []
    for i, robot in enumerate(robots):
        y_values.append(robot.y)
        x_values.append(robot.x)
    return float(calc_variation(y_values)), float(calc_variation(x_values))


def variances_to_outlier_sequences(y_variances: list[float], x_variances: list[float]) -> tuple[list[int], list[int]]:
    y_cutoff = (sum(y_variances) / len(y_variances)) / 2
    x_cutoff = (sum(x_variances) / len(x_variances)) / 2
    y_sequence = []
    x_sequence = []
    for i, (yv, xv) in enumerate(zip(y_variances, x_variances)):
        if yv < y_cutoff:
            y_sequence.append(i)
        if xv < x_cutoff:
            x_sequence.append(i)
    return y_sequence, x_sequence


def periodic_increase(sequence_sample: list[int]) -> Generator[[None], int]:
    a = sequence_sample[0]
    b = sequence_sample[1] - a
    for i in range(1, len(sequence_sample) - 1):
        j = i + 1
        assert (sequence_sample[j] - sequence_sample[i] == b), f'error in detecting periodic increase in {sequence_sample}'
    current = a
    while True:
        yield current
        current += b


def first_match_in_periodic_increase(left_sample: list[int], right_sample: list[int]) -> int:
    gen_left = periodic_increase(left_sample)
    gen_right = periodic_increase(right_sample)
    left = next(gen_left)
    right = next(gen_right)
    while left != right:
        if left < right:
            left = next(gen_left)
        else:
            right = next(gen_right)
    return left


def day14() -> None:

    start: float = time.perf_counter()

    PART1_STEPS = 100
    PART2_PATTERN_SAMPLE_STEPS = 250

    HEIGHT = 103
    WIDTH = 101

    robots: list[Robot] = []
    with open('../input/input14.txt') as file:
        for line in file:
            robots.append(Robot.parse(line))

    part1 = 0

    y_variance, x_variance = find_variance(robots)
    y_variances = [y_variance]
    x_variances = [x_variance]
    for step in range(1, PART2_PATTERN_SAMPLE_STEPS + 1):
        for robot in robots:
            robot.step(HEIGHT, WIDTH)
        y_variance, x_variance = find_variance(robots)
        y_variances.append(y_variance)
        x_variances.append(x_variance)
        if step == PART1_STEPS:
            part1 = do_part1_section_counts(robots, HEIGHT, WIDTH)

    y_sequence, x_sequence = variances_to_outlier_sequences(y_variances, x_variances)
    part2 = first_match_in_periodic_increase(y_sequence, x_sequence)

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 14 - Restroom Redoubt")
    print(f"Part 1: {part1}")
    assert 229868730 == part1
    print(f"Part 2: {part2}")
    assert 7861 == part2
    print(f"Time Taken: {stop-start:.6f} s")
