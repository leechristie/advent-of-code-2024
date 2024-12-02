// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#ifndef TIMING_H
#define TIMING_H

#include <time.h>

static volatile clock_t aoc_timer_begin;
static volatile clock_t aoc_timer_end;

static void start_timer() {
    aoc_timer_begin = clock();
}

static double stop_timer() {
    aoc_timer_end = clock();
    return (double) (aoc_timer_end - aoc_timer_begin) / CLOCKS_PER_SEC;
}

#endif //TIMING_H
