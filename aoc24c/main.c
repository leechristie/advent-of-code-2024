// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <stdio.h>
#include <string.h>

#include "days.h"

int main(const int argc, const char * argv[]) {

    if (argc < 2) {
        fputs("missing argument\n", stderr);
        return 1;
    }
    if (argc > 2) {
        fputs("too many arguments\n", stderr);
        return 1;
    }

    const char * day = argv[1];

    if (strcmp(day, "1") == 0) {
        return day01();
    }

    if (strcmp(day, "2") == 0) {
        return day02();
    }

    if (strcmp(day, "3") == 0) {
        return day03();
    }

    if (strcmp(day, "4") == 0) {
        return day04();
    }

    if (strcmp(day, "5") == 0) {
        return day05();
    }

    if (strcmp(day, "6") == 0) {
        return day06();
    }

    if (strcmp(day, "7") == 0) {
        return day07();
    }

    fprintf(stderr, "invalid day number \"%s\"", day);
    return 1;

}
