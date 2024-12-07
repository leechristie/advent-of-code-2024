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
static GuardState step(const CharGrid * const grid, int * const y, int * const x, int * const dy , int * const dx, CharGrid * const tracking) {
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
    assert(CharGrid_Get(grid, new_y, new_x) == '#' || CharGrid_Get(grid, new_y, new_x) == '.');
    if (CharGrid_Get(grid, new_y, new_x) == '#') {
        rotate_clockwise(dy, dx);
    } else {
        *y = new_y;
        *x = new_x;
    }
    return STILL_WALKING;
}

// returns true if the guard got into a loop
static GuardState trace_guard(const CharGrid * const grid, int y, int x, CharGrid * const tracking) {
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

int day06() {

    start_timer();

    int part1 = 0;
    int part2 = 0;

    // load the grid from the input file
    FILE * file = fopen("input06.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }
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
    GuardState part1_final_state = trace_guard(&grid, y, x, &tracking);
    if (part1_final_state != LEFT_GRID)
        FATAL_ERROR_EXIT("guard did not escape in first run");

    CharGrid_PrintHex(&tracking, true);  // DEBUGGING

    // anywhere the guard stepped must be counted for part 1
    part1 = CharGrid_CountNonZero(&tracking);

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
