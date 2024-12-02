// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <iostream>

#include "days.hpp"
#include "timing.hpp"

int main(const int argc, const char * argv[]) {

    if (argc < 2)
        throw std::invalid_argument("missing argument");
    if (argc > 2)
        throw std::invalid_argument("too many arguments");

    const std::string day {argv[1]};

    if (day == "1") {
        day01();
    } else if (day == "2")
        day02();
    else
        throw std::invalid_argument("invalid day number \"" + day + "\"");

    return 0;

}
