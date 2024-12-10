// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <ctype.h>
#include <stdio.h>

#include "days.h"
#include "grid.h"
#include "list.h"
#include "timing.h"

static int evaluate(const CharGrid * const grid, const int index, IntList * const visited_end_points, const char expected_symbol) {

    // invalid position
    if (index < 0)
        return 0;

    // wrong symbol
    const char actual_symbol = CharGrid_Get_ByIndex_OrDefault(grid, index, '\0');
    if (actual_symbol != expected_symbol)
        return 0;

    // found goal
    if (expected_symbol == '9') {
        IntList_SmallSet_Add(visited_end_points, index);
        return 1;
    }

    // not finished - check neighbours
    int rv = 0;
    rv += evaluate(grid, (int) CharGrid_Index_With_YXOffset(grid, index, -1, 0), visited_end_points, expected_symbol + 1);
    rv += evaluate(grid, (int) CharGrid_Index_With_YXOffset(grid, index, 0, 1), visited_end_points, expected_symbol + 1);
    rv += evaluate(grid, (int) CharGrid_Index_With_YXOffset(grid, index, 1, 0), visited_end_points, expected_symbol + 1);
    rv += evaluate(grid, (int) CharGrid_Index_With_YXOffset(grid, index, 0, -1), visited_end_points, expected_symbol + 1);
    return rv;

}

int day10() {

    start_timer();

    int part1 = 0;
    int part2 = 0;

    // read the grid
    FILE * file = fopen("input10.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }
    CharGrid grid;
    CharGrid_FromFile(&grid, file);
    fclose(file);

    // solve
    IntList visited_end_points;
    IntList_Init(&visited_end_points);
    for (int y = 0; y < (int) grid.height; y++) {
        for (int x = 0; x < (int) grid.width; x++) {
            int index = (int) CharGrid_YX_To_Index(&grid, y, x);
            part2 += evaluate(&grid, index, &visited_end_points, '0');
            part1 += (int) visited_end_points.length;
            IntList_Clear(&visited_end_points);
        }
    }

    // cleanup
    CharGrid_DeInit(&grid);
    IntList_DeInit(&visited_end_points);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 10 - Hoof It\n");
    printf("Part 1: %d\n", part1);
    printf("Part 2: %d\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}
