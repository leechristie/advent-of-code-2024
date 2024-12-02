// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#ifndef IO_H
#define IO_H
#include <assert.h>
#include <ctype.h>
#include <stdio.h>

static bool read_int(FILE * file, int * rv, int * term) {

    char current = '\0';

    // read until we find the first numeric digit
    while ((*term = fgetc(file)) != EOF) {
        assert(0 <= *term && *term <= 127);
        current = (char) *term;
        if (isdigit(current) || current == '-')
            break;
    }

    // reached EOF before finding any numeric character
    if (*term == EOF) {
        return false;
    }

    // set either the value or the negative flag
    int value = 0;
    bool negative = false;
    if (current == '-') {
        negative = true;
    } else {
        value = current - '0';
    }

    // read all remaining digits of the number
    while ((*term = fgetc(file)) != EOF) {
        assert(0 <= *term && *term <= 127);
        current = (char) *term;
        if (isdigit(current)) {
            value *= 10;
            value += current - '0';
        } else {
            break;
        }
    }

    // apply negative flag and return
    *rv = negative ? -value : value;
    return true;

}

#endif //IO_H
