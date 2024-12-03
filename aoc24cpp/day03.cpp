// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <fstream>
#include <iostream>
#include <regex>
#include <string>

#include "days.hpp"
#include "timing.hpp"

static std::string read_all(std::ifstream & file) {
    std::string all;
    std::string line;
    while (getline(file, line))
        all += line;
    return all;
}

void day03() {

    start_timer();

    int part1;
    int part2;
    {

        part1 = 0;
        part2 = 0;

        std::ifstream file {"input03.txt"};
        std::string all = read_all(file);

        std::regex pattern (R"(mul\((\d\d?\d?),(\d\d?\d?)\)|do\(\)|don't\(\))");

        bool enabled = true;

        const std::sregex_iterator end;
        for (auto iter = std::sregex_iterator(all.begin(), all.end(), pattern); iter != end; iter++) {

            const std::smatch & match = *iter;
            const std::string & str = match.str();

            // mul(###,###)
            if (str[0] == 'm') {

                const int product = stoi(match[1].str()) * stoi(match[2].str());
                part1 += product;
                if (enabled) {
                    part2 += product;
                }

            // do()
            } else if (str[2] == '(') {
                enabled = true;

            // don't()
            } else {
                enabled = false;
            }

        }

    }

    const double time = stop_timer();
    std::cout << "Advent of Code 2024" << std::endl;
    std::cout << "Day 3 - Mull It Over" << std::endl;
    std::cout << "Part 1: " << part1 << std::endl;
    std::cout << "Part 2: " << part2 << std::endl;
    std::cout << "Time Taken: " << std::fixed << std::setprecision(6) << time << " s" << std::endl;

}
