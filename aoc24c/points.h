// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#ifndef POINTS_H
#define POINTS_H

typedef struct Point2D {
    int y;
    int x;
} Point2D;

typedef struct Velocity2D {
    int dy;
    int dx;
} Velocity2D;

static const Velocity2D NORTH     = { .dy = -1, .dx =  0 };
static const Velocity2D NORTHEAST = { .dy = -1, .dx =  1 };
static const Velocity2D EAST      = { .dy =  0, .dx =  1 };
static const Velocity2D SOUTHEAST = { .dy =  1, .dx =  1 };
static const Velocity2D SOUTH     = { .dy =  1, .dx =  0 };
static const Velocity2D SOUTHWEST = { .dy =  1, .dx = -1 };
static const Velocity2D WEST      = { .dy =  0, .dx = -1 };
static const Velocity2D NORTHWEST = { .dy = -1, .dx = -1 };

static const Velocity2D DIRECTIONS[8] = { NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST };
static const Velocity2D HALF_DIRECTIONS[4] = { NORTH, NORTHEAST, EAST, SOUTHEAST };

#endif //POINTS_H
