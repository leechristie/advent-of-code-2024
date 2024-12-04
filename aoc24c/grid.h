// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#ifndef GRID_H
#define GRID_H

#include <stdio.h>
#include <assert.h>

#include "strings.h"

typedef struct CharGrid {
    char * data;
    size_t height;
    size_t width;
} CharGrid;

static void CharGrid_DeInit(CharGrid * const grid) {
    free(grid->data);
    grid->height = 0;
    grid->width = 0;
}

static void CharGrid_FromFile(CharGrid * const grid, FILE * const file) {
    StringBuffer buffer;
    StringBuffer_Init(&buffer);
    int current_line_width = 0;
    int width = 0;
    int height = 0;
    char c;
    while ((c = fgetc(file)) != EOF) {
        assert(c >= 0 && c < 127);
        const char current = (char) c;
        if (current == '\n') {
            assert(current_line_width > 0);
            assert(width == 0 || current_line_width == width);
            width = current_line_width;
            current_line_width = 0;
            height++;
        } else {
            assert('A' <= current && current <= 'Z');
            StringBuffer_Append(&buffer, current);
            current_line_width++;
        }
    }
    grid->data = buffer.data;  // ownership move
    grid->height = height;
    grid->width = width;
    /* don't DeInit StringBuffer */
}

static char CharGrid_Get_OrDefault(const CharGrid * const grid, const int y, const int x, const char default_char) {
    if (y < 0 || y >= (int) grid->height || x < 0 || x >= (int) grid->width)
        return default_char;
    return grid->data[(size_t) x + grid->width * (size_t) y];
}

static void CharGrid_Print(CharGrid * const grid, const size_t margin, const char default_char) {
    for (int y = - (int) margin; y < (int) grid->height + (int)  margin; y++) {
        for (int x = - (int) margin; x < (int) grid->width + (int) margin; x++) {
            putchar(CharGrid_Get_OrDefault(grid, y, x, default_char));
        }
        putchar('\n');
    }
    printf("height = %lu\n", grid->height);
    printf("width = %lu\n", grid->width);
}

#endif //GRID_H
