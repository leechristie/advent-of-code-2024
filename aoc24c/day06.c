// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <stdio.h>

#include "days.h"
#include "grid.h"
#include "timing.h"

typedef enum GuardState {
    STILL_WALKING = 0,
    LEFT_GRID = 1,
    CAUGHT_IN_LOOP = 2
} GuardState;

typedef enum DirectionTrail {
    NORTH = 1,
    EAST = 2,
    SOUTH = 4,
    WEST = 8
} DirectionTrail;

static DirectionTrail get_trail_direction(const int dy, const int dx) {
    assert(dx == 0 || dy == 0);
    assert(!(dx == 0 && dy == 0));
    assert(dx >= -1 && dx <= 1);
    assert(dy >= -1 && dx <= 1);
    if (dx == 0 && dy == -1)
        return NORTH;
    if (dx == 1 && dy == 0)
        return EAST;
    if (dx == 0 && dy == 1)
        return SOUTH;
    assert(dx == -1 && dy == 0);
    return WEST;
}

static void rotate_clockwise(int * const dy, int * const dx) {
    const int temp = *dy;
    *dy = *dx;
    *dx = -temp;
}

// returns false if the guard left the grid or
static GuardState step(const CharGrid * const grid, int * const y, int * const x, int * const dy , int * const dx, const CharGrid * const tracking) {
    assert(CharGrid_InBounds(grid, *y, *x));
    assert(CharGrid_Get(grid, *y, *x) == '.');
    const char old_tracking_mark = CharGrid_Get(tracking, *y, *x);
    const char tracking_mod = get_trail_direction(*dy, *dx);
    const char new_tracking_mark = (char) (old_tracking_mark | tracking_mod);
    if (new_tracking_mark == old_tracking_mark) {
        return CAUGHT_IN_LOOP;
    }
    CharGrid_Set(tracking, *y, *x, new_tracking_mark);
    const int new_y = *y + *dy;
    const int new_x = *x + *dx;
    if (!CharGrid_InBounds(grid, new_y, new_x)) {
        *y = new_y;
        *x = new_x;
        return LEFT_GRID;
    }
    assert(CharGrid_Get(grid, new_y, new_x) == '#' || CharGrid_Get(grid, new_y, new_x) == '.' || CharGrid_Get(grid, new_y, new_x) == 'O');
    const char at_location = CharGrid_Get(grid, new_y, new_x);
    if (at_location == '#' || at_location == 'O') {
        rotate_clockwise(dy, dx);
    } else {
        *y = new_y;
        *x = new_x;
    }
    return STILL_WALKING;
}

// returns true if the guard got into a loop
static GuardState trace_guard(const CharGrid * const grid, int y, int x, const CharGrid * const tracking) {
    int dy = -1;
    int dx = 0;
    CharGrid_Clear(tracking);
    GuardState state = STILL_WALKING;
    while (state == STILL_WALKING) {
        state = step(grid, &y, &x, &dy, &dx, tracking);
    }
    assert(state == LEFT_GRID || state == CAUGHT_IN_LOOP);
    return state;
}

static void solve(const CharGrid * const grid, const CharGrid * const tracking, const int start_y, const int start_x, int * const part1, int * const part2) {

    // new grid for simulations
    CharGrid tracking_with_obstacle;
    CharGrid_Init(&tracking_with_obstacle, grid->height, grid->width);

    for (int y = 0; y < (int) tracking->height; y++) {
        for (int x = 0; x < (int) tracking->width; x++) {
            if (CharGrid_Get(tracking, y, x) != 0) {

                // count this square as a location the guard walked on in Part 1
                (*part1)++;

                // Only check Part 2 if not tje start (we can't put the obstacle on the guard)
                if (start_y != y || start_x != x) {

                    assert(CharGrid_Get(grid, y, x) == '.');
                    CharGrid_Set(grid, y, x, 'O');
                    assert(CharGrid_Count(grid, 'O') == 1);
                    const GuardState state = trace_guard(grid, start_y, start_x, &tracking_with_obstacle);
                    CharGrid_Set(grid, y, x, '.');
                    assert(CharGrid_Count(grid, 'O') == 0);
                    assert(state == LEFT_GRID || state == CAUGHT_IN_LOOP);
                    if (state == CAUGHT_IN_LOOP)
                        (*part2)++;

                }

            }
        }
    }

    // cleanup temp grid
    CharGrid_DeInit(&tracking_with_obstacle);

}

int day06() {

    start_timer();

    int part1 = 0;
    int part2 = 0;

    // open the input file
    FILE * file = fopen("input06.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }

    // load the grid from the input file
    CharGrid grid;
    int y;
    int x;
    CharGrid_FromFile_WithSpecialChar(&grid, file, '^', &y, &x);
    fclose(file);

    // remove the start symbol so we have a clean grid
    CharGrid_Set(&grid, y, x, '.');

    // create a grid for following the movements of the guard
    CharGrid tracking;
    CharGrid_Init(&tracking, grid.height, grid.width);

    // track the motions of the guard on the first part - no extra block, expect leaving grid
    trace_guard(&grid, y, x, &tracking);

    // loop over the trail to solve both parts
    solve(&grid, &tracking, y, x, &part1, &part2);

    // cleanup
    CharGrid_DeInit(&grid);
    CharGrid_DeInit(&tracking);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 6 - Guard Gallivant\n");
    printf("Part 1: %d\n", part1);
    printf("Part 2: %d\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}
