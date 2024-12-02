// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>

#include "days.hpp"
#include "timing.hpp"

static bool read_report(std::ifstream & file, std::string buffer, std::vector<int> & report) {

    buffer.clear();
    report.clear();

    getline(file, buffer);

    std::stringstream buffered_stream {buffer};

    int value;
    while (buffered_stream >> value)
        report.push_back(value);

    return !report.empty();

}

bool report_is_safe(const std::vector<int> & report) {
    if (report.size() < 2)
        return true;
    bool increase = false;
    bool decrease = false;
    for (std::vector<int>::size_type i = 0; i < report.size() - 1; i++) {
        const std::vector<int>::size_type j = i + 1;
        const int first = report[i];
        const int second = report[j];
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

bool report_is_safe(const std::vector<int> & report, const std::vector<int>::size_type ignored_index) {
    assert(ignored_index < report.size());
    assert(!report.empty());  // must be non-empty to ignore an index
    const std::vector<int>::size_type apparent_size = report.size() - 1;
    if (apparent_size < 2)
        return true;
    bool increase = false;
    bool decrease = false;
    for (std::vector<int>::size_type i = 0; i < report.size() - 1; i++) {

        // check for ignored current
        if (i == ignored_index)
            continue;

        // find next index with shift if ignored
        std::vector<int>::size_type j = i + 1;
        if (j == ignored_index) {
            j++;
            if (j >= report.size())
                continue;
        }

        const int first = report[i];
        const int second = report[j];
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

bool unsafe_report_is_repairable(const std::vector<int> & report) {

    // if the report is only 2 items, we can remove either and it is fixed
    if (report.size() < 3) {
        assert(report.size() == 2);  // we should only get here if == 2
        return true;
    }

    // brute force solution
    for (std::vector<int>::size_type i = 0; i < report.size(); i++) {
        if (report_is_safe(report, i)) {
            return true;
        }
    }
    return false;

}

void day02() {

    start_timer();

    int part1;
    int part2;
    {

        part1 = 0;
        part2 = 0;

        std::ifstream file {"input02.txt"};

        std::string buffer;
        std::vector<int> report;
        while (read_report(file, buffer, report)) {
            const bool safe = report_is_safe(report);
            if (safe) {
                part1++;
                part2++;
            } else {
                if (unsafe_report_is_repairable(report))
                    part2++;
            }
        }

    }

    const double time = stop_timer();
    std::cout << "Advent of Code 2024" << std::endl;
    std::cout << "Day 2 - Red-Nosed Reports" << std::endl;
    std::cout << "Part 1: " << part1 << std::endl;
    std::cout << "Part 2: " << part2 << std::endl;
    std::cout << "Time Taken: " << std::fixed << std::setprecision(6) << time << " s" << std::endl;

}
