// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#ifndef FATAL_H
#define FATAL_H

#define FATAL(message) do {fprintf(stderr, "ABORTING - FATAL ERROR: %s\n", message); exit(1);} while(false);

#endif //FATAL_H
