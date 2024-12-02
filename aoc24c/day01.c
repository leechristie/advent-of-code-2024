// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <stdio.h>

#include "days.h"
#include "list.h"
#include "io.h"

static void read_lists(FILE * file, IntList * const left, IntList * const right) {
    int value;
    int unused;
    while (read_int(file, &value, &unused)) {
        IntList_Append(left, value);
        const bool got_pair = read_int(file, &value, &unused);
        if (got_pair)
            IntList_Append(right, value);
        assert(got_pair);  // make sure we got a pair of numbers
    }
}

static int sum_abs_differences(const IntList * const left, const IntList * const right) {
    assert(left->length == right->length);
    const size_t length = left->length;
    int total = 0;
    for (size_t i = 0; i < length; i++) {
        const int l = left->ptrBuffer[i];
        const int r = right->ptrBuffer[i];
        const int diff = abs(l - r);
        total += diff;
    }
    return total;
}

static int sum_similarity_scores(const IntList * const left, const IntList * const right) {
    assert(left->length == right->length);
    const size_t length = left->length;
    int total = 0;
    for (size_t i = 0; i < length; i++) {
        const int item = left->ptrBuffer[i];
        const int count_right = IntList_Sorted_CountOf(right, item);
        total += item * count_right;
    }
    return total;
}

int day01() {

    printf("Advent of Code 2024\n");
    printf("Day 1\n");

    FILE * file = fopen("input01.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }

    IntList left;
    IntList_Init(&left);
    IntList right;
    IntList_Init(&right);

    read_lists(file, &left, &right);
    fclose(file);

    IntList_Sort(&left);
    IntList_Sort(&right);

    const int part1 = sum_abs_differences(&left, &right);
    printf("Part 1: %d\n", part1);

    const int part2 = sum_similarity_scores(&left, &right);
    printf("Part 2: %d\n", part2);

    IntList_DeInit(&left);
    IntList_DeInit(&right);

    return 0;

}
