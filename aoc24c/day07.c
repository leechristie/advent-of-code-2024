// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <limits.h>
#include <stdio.h>

#include "days.h"
#include "grid.h"
#include "io.h"
#include "list.h"
#include "timing.h"

static bool can_be_true_recursive(const long target, const IntList * const numbers, const size_t first_index, const long cumulative) {

    // check if exceeded the target
    if (cumulative > target)
        return false;

    // check if reached end of list
    if (first_index >= numbers->length)
        return target == cumulative;

    // case when the next operation is a multiply
    const long cumulative_with_multiply = cumulative * numbers->ptrBuffer[first_index];
    if (can_be_true_recursive(target, numbers, first_index + 1, cumulative_with_multiply))
        return true;

    // case when the next operation is an add
    const long cumulative_with_add = cumulative + numbers->ptrBuffer[first_index];
    return can_be_true_recursive(target, numbers, first_index + 1, cumulative_with_add);

}

static bool can_be_true(const long target, const IntList * const numbers) {
    return can_be_true_recursive(target, numbers, 1, numbers->ptrBuffer[0]);
}

static bool can_be_true_with_concat_recursive(const long target, const IntList * const numbers, const size_t first_index, long cumulative) {

    // check if exceeded the target
    if (cumulative > target)
        return false;

    // check if reached end of list
    if (first_index >= numbers->length)
        return target == cumulative;

    // case when the next operation is a multiply
    const long cumulative_with_multiply = cumulative * numbers->ptrBuffer[first_index];
    if (can_be_true_with_concat_recursive(target, numbers, first_index + 1, cumulative_with_multiply))
        return true;

    // case when the next operation is an add
    const long cumulative_with_add = cumulative + numbers->ptrBuffer[first_index];
    if (can_be_true_with_concat_recursive(target, numbers, first_index + 1, cumulative_with_add))
        return true;

    // case when the next operation is a concat
    long temp = numbers->ptrBuffer[first_index];
    while (temp > 0) {
        temp /= 10;
        cumulative *= 10;
    }
    return can_be_true_with_concat_recursive(target, numbers, first_index + 1, cumulative + numbers->ptrBuffer[first_index]);

}

static bool can_be_true_with_concat(long target, IntList * numbers) {
    return can_be_true_with_concat_recursive(target, numbers, 1, numbers->ptrBuffer[0]);
}

int day07() {

    start_timer();

    long part1 = 0;
    long part2 = 0;

    // open the input file
    FILE * file = fopen("input07.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }

    IntList numbers;
    IntList_Init(&numbers);

    long target;
    int term;
    read_long(file, &target, &term);
    while (IntList_ReadCSV_Custom_Sep(file, &numbers, ' ')) {
        if (can_be_true(target, &numbers)) {
            part1 += target;
            part2 += target;
        } else {
            if (can_be_true_with_concat(target, &numbers))
                part2 += target;
        }
        if (!read_long(file, &target, &term)) {
            break;
        }
    }

    IntList_DeInit(&numbers);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 7 - Bridge Repair\n");
    printf("Part 1: %ld\n", part1);
    printf("Part 2: %ld\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}
