// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>

#include "days.hpp"

static void read_lists(std::ifstream & file, std::vector<int> & left_list, std::vector<int> & right_list) {

    int left, right;

    while (file >> left) {
        left_list.push_back(left);
        if (file >> right)
            right_list.push_back(right);
        else
            throw std::invalid_argument("missing pair of numbers");
    }

}

static int sum_abs_differences(const std::vector<int> & left, const std::vector<int> & right) {
    assert(left.size() == right.size());
    const std::vector<int>::size_type length = left.size();
    int total = 0;
    for (std::vector<int>::size_type i = 0; i < length; i++) {
        const int l = left[i];
        const int r = right[i];
        const int diff = abs(l - r);
        total += diff;
    }
    return total;
}

static std::vector<int>::size_type count_sorted_vector(const std::vector<int> & list, const int value) {
    const auto lower = std::ranges::lower_bound(list, value);
    const auto upper = std::ranges::upper_bound(list, value);
    return upper - lower;
}

static int sum_similarity_scores(const std::vector<int> & left, const std::vector<int> & right) {
    int total = 0;
    for (auto value: left)
        total += static_cast<int>(value * count_sorted_vector(right, value));
    return total;
}

void day01() {

    std::ifstream file {"input01.txt"};

    std::vector<int> left;
    std::vector<int> right;

    read_lists(file, left, right);
    assert(left.size() == right.size());

    std::ranges::sort(left);
    std::ranges::sort(right);

    const int part1 = sum_abs_differences(left, right);
    const int part2 = sum_similarity_scores(left, right);

    std::cout << "Advent of Code 2024" << std::endl;
    std::cout << "Day 1" << std::endl;
    std::cout << "Part 1: " << part1 << std::endl;
    std::cout << "Part 2: " << part2 << std::endl;

}
