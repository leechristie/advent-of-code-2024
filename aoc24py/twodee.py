# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


from dataclasses import dataclass


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
        return abs(other.y - self.y) + abs(other.x - self.x)


@dataclass(eq=True, frozen=True)
class State:
    point: Point
    facing: Facing
