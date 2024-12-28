// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <ctype.h>
#include <stdio.h>

#include "strings.h"
#include "timing.h"

#define MAX_PATTERN_LENGTH (8)
#define MAX_PATTERNS (500)
#define MAX_TARGET_LENGTH (60)

static char patterns[MAX_PATTERNS + 1][MAX_PATTERN_LENGTH + 1];
static StringBuffer target;

static void read_patterns(FILE * const file) {
    int pattern_index = 0;
    int character_index = 0;
    int c = getc(file);
    while (true) {
        if (c == ',' || c == '\n') {
            patterns[pattern_index][character_index] = '\0';
            if (c == '\n') {
                patterns[pattern_index + 1][0] = '\0';
                break;
            }
            pattern_index++;
            character_index = 0;
        } else if (c == ' ') {
            // nothing
        } else {
            assert(pattern_index < MAX_PATTERNS);
            assert(character_index < MAX_PATTERN_LENGTH);
            assert(isalpha(c));
            patterns[pattern_index][character_index] = (char) c;
            character_index++;
        }
        c = getc(file);
    }
}

bool read_line(FILE * const file, StringBuffer * const buffer) {
    StringBuffer_Clear(buffer);
    while (true) {
        const int c = getc(file);
        if (c == '\n' || c == EOF) {
            return buffer->length > 0;
        }
        StringBuffer_Append(buffer, (char) c);
    }
}

static long long memoized_result[MAX_TARGET_LENGTH] = {-1};

static size_t fits_here(const size_t next_match_index, const int lower) {
    size_t index = 0;
    char symbol = patterns[next_match_index][index];
    while (symbol != '\0') {
        const char match_symbol = target.data[index + lower];
        if (match_symbol == '\0') {
            return 0;
        }
        if (match_symbol != symbol) {
            return 0;
        }
        index++;
        symbol = patterns[next_match_index][index];
    }
    return index;
}

static long long ways_of_tail_matching(const size_t lower) {
    assert(lower < MAX_TARGET_LENGTH);
    if (memoized_result[lower] != -1) {
        return memoized_result[lower];
    }
    if (target.data[lower] == '\0') {
        return 1;
    }
    size_t found_match_next_tails[MAX_PATTERNS + 1] = {0};
    size_t num_matches = 0;
    size_t next_match_index = 0;
    while (patterns[next_match_index][0] != '\0') {
        const size_t offset = fits_here(next_match_index, lower);
        if (offset) {
            found_match_next_tails[num_matches++] = lower + offset;
        }
        next_match_index++;
    }
    if (num_matches == 0) {
        return 0;
    }
    long long rv = 0;
    for (size_t i = 0; i < num_matches; i++) {
        assert(found_match_next_tails[i] > 0);
        rv += ways_of_tail_matching(found_match_next_tails[i]);
    }
    memoized_result[lower] = rv;
    return rv;
}

int day19() {

    start_timer();

    int part1 = 0;
    long long part2 = 0;

    FILE * file = fopen("input19.txt", "r");
    if (file == NULL) {
        printf("unable to open input file");
        return 1;
    }

    // read the patterns
    read_patterns(file);

    // read blank line
    getc(file);

    // for each target
    StringBuffer_Init(&target);
    while (read_line(file, &target)) {
        assert(target.length <= MAX_TARGET_LENGTH);
        for (size_t i = 0; i < MAX_TARGET_LENGTH; i++) {
            memoized_result[i] = -1;
        }
        long long ways = ways_of_tail_matching(0);
        if (ways > 0) {
            part1++;
        }
        part2 += ways;
    }
    StringBuffer_DeInit(&target);

    fclose(file);

    const double time = stop_timer();
    printf("Advent of Code 2024\n");
    printf("Day 19 - Linen Layout\n");
    printf("Part 1: %d\n", part1);
    printf("Part 2: %lld\n", part2);
    printf("Time Taken: %.6f s\n", time);
    return 0;

}
