// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <stdio.h>

#include "days.h"
#include "io.h"
#include "list.h"
#include "timing.h"

#define NO_IGNORED_INDEX (-1)

bool read_report(FILE * file, IntList * report) {

    int value;
    int term = '\0';

    IntList_Clear(report);

    // reading the first character
    // will return false if no numbers is read
    if (read_int(file, &value, &term)) {
        assert(term == '\n' || term == EOF || term == ' ');
        IntList_Append(report, value);
        if (term == '\n' || term == EOF)
            return true;
        assert(term == ' ');
    } else {
        assert(term == EOF);
        return false;
    }

    // read the remaining characters until EOF or new line
    // always return true
    while (read_int(file, &value, &term)) {
        assert(term == '\n' || term == EOF || term == ' ');
        IntList_Append(report, value);
        if (term == '\n' || term == EOF)
            return true;
        assert(term == ' ');
    }
    assert(term == EOF);
    return true;

}

bool report_is_safe(const IntList * const report, const ssize_t ignored_index) {
    assert(report->length >= 3);
    const bool ignoring = ignored_index != NO_IGNORED_INDEX;
    if (ignoring) {
        assert(ignored_index >= 0);
        assert(report->length >= 3);
    } else {
        assert(report->length >= 2);
    }
    bool increase = false;
    bool decrease = false;
    for (size_t i = 0; i < report->length - 1; i++) {

        // check for ignored current
        if (ignoring && (i == (size_t) ignored_index))
            continue;

        // find next index with shift if ignored
        size_t j = i + 1;
        if (ignoring && (j == (size_t) ignored_index)) {
            j++;
            if (j >= report->length)
                continue;
        }

        const int first = report->ptrBuffer[i];
        const int second = report->ptrBuffer[j];
        const int abs_diff = abs(first - second);
        if (abs_diff == 0)
            return false;  // must increase or decrease
        if (abs_diff > 3)
            return false;  // unsafe due to increasing or decreasing too fast
        if (second > first)
            increase = true;
        else
            decrease = true;

    }
    assert(increase || decrease);  // will always increase or decrease due to earlier check
    return !(increase && decrease);  // safe if always going one way
}

bool unsafe_report_is_repairable(IntList * report) {

    // if the report is only 2 items, we can remove either and it is fixed
    if (report->length < 3) {
        assert(report->length == 2);  // we should only get here if == 2
        return true;
    }

    // brute force solution
    for (size_t i = 0; i < report->length; i++) {
        if (report_is_safe(report, (ssize_t) i)) {
            return true;
        }
    }
    return false;

}

int day02() {

    start_timer();

    FILE * file = fopen("input02.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }

    IntList report;
    IntList_Init(&report);

    int part1 = 0;
    int part2 = 0;
    while (read_report(file, &report)) {
        const bool safe = report_is_safe(&report, NO_IGNORED_INDEX);
        if (safe) {
            part1++;
            part2++;
        } else {
            if (unsafe_report_is_repairable(&report))
                part2++;
        }
    }

    fclose(file);
    IntList_DeInit(&report);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 2 - Red-Nosed Reports\n");
    printf("Part 1: %d\n", part1);
    printf("Part 2: %d\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}
