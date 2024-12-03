// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#ifndef TIMING_H
#define TIMING_H

#include <time.h>

static volatile struct timespec aoc_timer_begin;
static volatile struct timespec aoc_timer_end;

static void start_timer() {
    clock_gettime(CLOCK_MONOTONIC, (struct timespec *) &aoc_timer_begin);
}

static double stop_timer() {
    clock_gettime(CLOCK_MONOTONIC, (struct timespec *) &aoc_timer_end);
    const long long ns = 1000000000LL * (aoc_timer_end.tv_sec - aoc_timer_begin.tv_sec)
            + aoc_timer_end.tv_nsec - aoc_timer_begin.tv_nsec;
    return (double) ns / 1000000000LL;
}

#endif //TIMING_H
