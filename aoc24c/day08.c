// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <stdio.h>

#include "days.h"
#include "grid.h"
#include "io.h"
#include "list.h"
#include "timing.h"

#define NUM_SYMBOLS (62)
#define START_INDEX_DIGITS (0)
#define START_INDEX_LOWER (10)
#define START_INDEX_UPPER (36)

static size_t symbol_to_index(const char symbol) {
    assert(isdigit(symbol) || islower(symbol) || isupper(symbol));
    if (isdigit(symbol))
        return symbol - '0' + START_INDEX_DIGITS;
    if (islower(symbol))
        return symbol - 'a' + START_INDEX_LOWER;
    return symbol - 'A' + START_INDEX_UPPER;
}

static void write_antinodes_simple(const CharGrid * const grid, const int ay, const int ax, const int by, const int bx) {
    const int dy = by - ay;
    const int dx = bx - ax;
    CharGrid_Set_OrIgnore(grid, ay - dy, ax - dx, '#');
    CharGrid_Set_OrIgnore(grid, by + dy, bx + dx, '#');
}

static void write_antinodes_extended(const CharGrid * const grid, const int ay, const int ax, const int by, const int bx) {
    CharGrid_Set_OrIgnore(grid, ay, ax, '#');
    CharGrid_Set_OrIgnore(grid, by, bx, '#');
    const int dy = by - ay;
    const int dx = bx - ax;
    int y = by + dy;
    int x = bx + dx;
    while (CharGrid_Set_OrIgnore(grid, y, x, '#')) {
        y += dy;
        x += dx;
    }
    y = ay - dy;
    x = ax - dx;
    while (CharGrid_Set_OrIgnore(grid, y, x, '#')) {
        y -= dy;
        x -= dx;
    }
}

int day08() {

    start_timer();

    // read the grid
    FILE * file = fopen("input08.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }
    CharGrid grid1;
    CharGrid_FromFile(&grid1, file);
    fclose(file);

    // another grid to write Part 2
    CharGrid grid2;
    CharGrid_Init_Fill(&grid2, grid1.height, grid1.width, '.');

    // create 36 list to map symbols to set of locations
    IntList location_map[NUM_SYMBOLS];
    for (size_t i = 0; i < NUM_SYMBOLS; i++)
        IntList_Init(&location_map[i]);

    // add locations of each character
    for (size_t i = 0; i < CharGrid_Area(&grid1); i++) {
        const char symbol = grid1.data[i];
        if (symbol != '.') {
            const size_t index = symbol_to_index(symbol);
            IntList_Append(&location_map[index], (int) i);
        }
    }

    // loop over all pairs of matching symbols
    for (size_t i = 0; i < NUM_SYMBOLS; i++) {
        if (location_map[i].length > 0) {
            for (size_t j = 0; j < location_map[i].length - 1; j++) {
                int a = location_map[i].ptrBuffer[j];
                int ay;
                int ax;
                CharGrid_Index_To_YX(&grid1, a, &ay, &ax);
                for (size_t k = j + 1; k < location_map[i].length; k++) {
                    int b = location_map[i].ptrBuffer[k];
                    int by;
                    int bx;
                    CharGrid_Index_To_YX(&grid1, b, &by, &bx);
                    write_antinodes_simple(&grid1, ay, ax, by, bx);    // Part 1 rule set
                    write_antinodes_extended(&grid2, ay, ax, by, bx);  // Part 2 rule set
                }
            }
        }
    }

    // count the antinodes
    const int part1 = CharGrid_Count(&grid1, '#');
    const int part2 = CharGrid_Count(&grid2, '#');

    // cleanup
    CharGrid_DeInit(&grid1);
    CharGrid_DeInit(&grid2);
    for (size_t i = 0; i < NUM_SYMBOLS; i++)
        IntList_DeInit(&location_map[i]);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 8 - Resonant Collinearity\n");
    printf("Part 1: %d\n", part1);
    printf("Part 2: %d\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}
