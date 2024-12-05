// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <assert.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

#include "fatal.h"
#include "list.h"
#include "timing.h"

#define BOUND (100)

static void write_cell(signed char * orders, const size_t y, const size_t x, const signed char value) {
    orders[(y * BOUND) + x] = value;
}

static signed char read_cell(const signed char * orders, const size_t y, const size_t x) {
    return orders[(y * BOUND) + x];
}

static void read_orders(FILE * const file, signed char * const orders) {

    int c;
    size_t first_number = 0;
    size_t second_number = 0;
    while ((c = fgetc(file)) != EOF) {

        char character = (char) c;
        if (character == '\n')
            return;

        // first digit in first number
        assert(isdigit(character) && character >= '1');
        first_number = 10 * (character - '0');

        // second digit in first number
        c = fgetc(file);
        if (c == EOF)
            break;
        character = (char) c;
        assert(isdigit(character));
        first_number += character - '0';

        // separator |
        c = fgetc(file);
        if (c == EOF)
            break;
        character = (char) c;
        assert(character == '|');

        // first digit in second number
        c = fgetc(file);
        if (c == EOF)
            break;
        character = (char) c;
        assert(isdigit(character) && character >= '1');
        second_number = 10 * (character - '0');

        // second digit in second number
        c = fgetc(file);
        if (c == EOF)
            break;
        character = (char) c;
        assert(isdigit(character));
        second_number += character - '0';

        // separator |
        c = fgetc(file);
        if (c == EOF)
            break;
        character = (char) c;
        assert(character == '\n');

        // record order both ways
        write_cell(orders, first_number, second_number, -1);
        write_cell(orders, second_number, first_number, 1);

    }
    FATAL_ERROR_EXIT("got EOF in read_orders");
}

static bool is_correctly_ordered(const IntList * const list, const signed char * const orders) {
    for (size_t i = 0; i < list->length - 1; i++) {
        const size_t j = i + 1;
        const int a = list->ptrBuffer[i];
        const int b = list->ptrBuffer[j];
        const signed char cmp_value = read_cell(orders, a, b);
        assert(cmp_value == -1 || cmp_value == 1);
        assert(a != b);
        if (cmp_value == 1)
            return false;
    }
    return true;
}

static int middle_element(const IntList * const list) {
    assert(list->length % 2 == 1);
    return list->ptrBuffer[list->length / 2];
}

static signed char * COMPARE_BY_INT;

static int compare_by_order(const void * ptrA, const void * ptrB) {
    const size_t a = (size_t) (*(int *) ptrA);
    const size_t b = (size_t) (*(int *) ptrB);
    const signed char cmp = read_cell(COMPARE_BY_INT, a, b);
    assert((a == b && cmp == 0) || ((a != b) && (cmp == -1 || cmp == 1)));
    return cmp;
}

int day05() {

    start_timer();

    int part1 = 0;
    int part2 = 0;

    FILE * file = fopen("input05.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }

    signed char orders[BOUND * BOUND] = {0};

    // ReSharper disable once CppDFALocalValueEscapesFunction
    COMPARE_BY_INT = orders;

    read_orders(file, orders);

    IntList current;
    IntList_Init(&current);
    while (IntList_ReadCSV(file, &current)) {
        if (is_correctly_ordered(&current, orders)) {
            part1 += middle_element(&current);
        } else {
            IntList_Sort_Custom(&current, compare_by_order);
            part2 += middle_element(&current);
        }
    }
    IntList_DeInit(&current);

    COMPARE_BY_INT = nullptr;

    fclose(file);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 5 - Print Queue\n");
    printf("Part 1: %d\n", part1);
    printf("Part 2: %d\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}

