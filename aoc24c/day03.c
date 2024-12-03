// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <stdio.h>

#include "days.h"
#include "timing.h"

#include <unistd.h>

int day03() {

    for (int i = 0; i < 10; i++) {
        start_timer();

        sleep(2);

        const double time = stop_timer();
        printf("Time Taken: %.6f s\n", time);
    }

    return 0;

}
