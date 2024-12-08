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

static void CharGrid_Init(CharGrid * const grid, const size_t height, const size_t width) {
    grid->data = (char *) malloc(sizeof(char) * width * height);
    for (size_t i = 0; i < height * width; i++) {
        grid->data[i] = 0;
    }
    grid->height = height;
    grid->width = width;
}

static void CharGrid_Init_Fill(CharGrid * const grid, const size_t height, const size_t width, const char fill) {
    grid->data = (char *) malloc(sizeof(char) * width * height);
    for (size_t i = 0; i < height * width; i++) {
        grid->data[i] = fill;
    }
    grid->height = height;
    grid->width = width;
}

static void CharGrid_Clear(const CharGrid * const grid) {
    for (size_t i = 0; i < grid->height * grid->width; i++) {
        grid->data[i] = 0;
    }
}

static void CharGrid_DeInit(CharGrid * const grid) {
    free(grid->data);
    grid->height = 0;
    grid->width = 0;
}

static void CharGrid_FromFile_WithSpecialChar(CharGrid * const grid, FILE * const file, const char special, int * const y, int * const x) {
    StringBuffer buffer;
    StringBuffer_Init(&buffer);
    int current_line_width = 0;
    int width = 0;
    int height = 0;
    *y = -1;
    *x = -1;
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
            if (current == special) {
                assert(*x == -1 && *y == -1);
                *y = height;
                *x = current_line_width;
            }
            StringBuffer_Append(&buffer, current);
            current_line_width++;
        }
    }
    grid->data = buffer.data;  // ownership move
    grid->height = height;
    grid->width = width;
    /* don't DeInit StringBuffer */
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
            StringBuffer_Append(&buffer, current);
            current_line_width++;
        }
    }
    grid->data = buffer.data;  // ownership move
    grid->height = height;
    grid->width = width;
    /* don't DeInit StringBuffer */
}

static bool CharGrid_InBounds(const CharGrid * grid, int y, int x) {
    return !(y < 0 || y >= (int) grid->height || x < 0 || x >= (int) grid->width);
}

static char CharGrid_Get_OrDefault(const CharGrid * const grid, const int y, const int x, const char default_char) {
    if (!CharGrid_InBounds(grid, y, x))
        return default_char;
    return grid->data[(size_t) x + grid->width * (size_t) y];
}

static char CharGrid_Get(const CharGrid * const grid, const int y, const int x) {
    assert(CharGrid_InBounds(grid, y, x));
    return grid->data[(size_t) x + grid->width * (size_t) y];
}

static void CharGrid_Index_To_YX(const CharGrid * const grid, const int index, int * const y, int * const x) {
    *y = index / grid->width;
    *x = index % grid->width;
    assert(CharGrid_InBounds(grid, *y, *x));
}

static void CharGrid_Set(const CharGrid * const grid, const int y, const int x, const char value) {
    assert(CharGrid_InBounds(grid, y, x));
    grid->data[(size_t) x + grid->width * (size_t) y] = value;
}

static bool CharGrid_Set_OrIgnore(const CharGrid * const grid, const int y, const int x, const char value) {
    if (CharGrid_InBounds(grid, y, x)) {
        grid->data[(size_t) x + grid->width * (size_t) y] = value;
        return true;
    }
    return false;
}

static int CharGrid_CountNonZero(const CharGrid * const grid) {
    int rv = 0;
    for (int y = 0; y < (int) grid->height; y++)
        for (int x = 0; x < (int) grid->width; x++)
            if (CharGrid_Get(grid, y, x) != 0)
                rv++;
    return rv;
}

static int CharGrid_Count(const CharGrid * const grid, const char value) {
    int rv = 0;
    for (int y = 0; y < (int) grid->height; y++)
        for (int x = 0; x < (int) grid->width; x++)
            if (CharGrid_Get(grid, y, x) == value)
                rv++;
    return rv;
}

static size_t CharGrid_Area(const CharGrid * const grid) {
    return grid->height * grid->width;
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

static void CharGrid_PrintHex(CharGrid * const grid, const bool hide_zero) {
    for (int y = 0; y < (int) grid->height; y++) {
        for (int x = 0; x < (int) grid->width; x++) {
            if (x != 0) {
                putchar(' ');
            }
            char c = CharGrid_Get_OrDefault(grid, y, x, '\0');
            assert(c >= 0 && c < 127);
            if (hide_zero && c == 0) {
                printf("  ");
            } else {
                printf("%02x", c);
            }
        }
        putchar('\n');
    }
    printf("height = %lu\n", grid->height);
    printf("width = %lu\n", grid->width);
}

#endif //GRID_H
