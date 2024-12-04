// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <stdio.h>

#include "days.h"
#include "strings.h"
#include "timing.h"
#include "points.h"
#include "grid.h"

static void GetWordSearchWord(const CharGrid * const grid, StringBuffer * const buffer, int y, int x, const Velocity2D * const direction, const size_t length) {
    StringBuffer_Clear(buffer);
    for (size_t i = 0; i < length; i++) {
        StringBuffer_Append(buffer, CharGrid_Get_OrDefault(grid, y, x, '\0'));
        y += direction->dy;
        x += direction->dx;
    }
}

int day04() {

    start_timer();

    FILE * file = fopen("input04.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }

    int part1 = 0;
    int part2 = 0;

    CharGrid grid;
    CharGrid_FromFile(&grid, file);

    const char TARGET_PART1[] = "XMAS";
    const char TARGET_PART1_REVERSE[] = "SAMX";
    const char TARGET_PART2[] = "MAS";
    const char TARGET_PART2_REVERSE[] = "SAM";

    StringBuffer string_buffer;
    StringBuffer_Init(&string_buffer);
    for (int y = 0; y < (int) grid.height; y++) {
        for (int x = 0; x < (int) grid.width; x++) {

            // Part 1
            for (size_t d = 0; d < 4; d++) {
                GetWordSearchWord(&grid, &string_buffer, y, x, &HALF_DIRECTIONS[d], 4);
                if (strcmp(string_buffer.data, TARGET_PART1) == 0 || strcmp(string_buffer.data, TARGET_PART1_REVERSE) == 0) {
                    part1++;
                }
            }

            // Part 2
            GetWordSearchWord(&grid, &string_buffer, y-1, x-1, &SOUTHEAST, 3);
            bool nw_to_se_is_mas = strcmp(string_buffer.data, TARGET_PART2) == 0 || strcmp(string_buffer.data, TARGET_PART2_REVERSE) == 0;
            if (nw_to_se_is_mas) {
                GetWordSearchWord(&grid, &string_buffer, y-1, x+1, &SOUTHWEST, 3);
                bool ne_to_sw_is_mas = strcmp(string_buffer.data, TARGET_PART2) == 0 || strcmp(string_buffer.data, TARGET_PART2_REVERSE) == 0;
                if (ne_to_sw_is_mas)
                    part2++;
            }

        }
    }
    StringBuffer_DeInit(&string_buffer);

    CharGrid_DeInit(&grid);
    fclose(file);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 4 - Ceres Search\n");
    printf("Part 1: %d\n", part1);
    printf("Part 2: %d\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}
