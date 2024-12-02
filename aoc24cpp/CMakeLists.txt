cmake_minimum_required(VERSION 3.30)
project(aoc24cpp)

set(CMAKE_CXX_STANDARD 23)

set(COMMON_FLAGS "${COMMON_FLAGS} -Wall -Wno-unused-function -Wextra -Wpedantic -Werror")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} ${COMMON_FLAGS} -g3 -O0 -fsanitize=address,undefined -fno-omit-frame-pointer -fstack-protector-strong -fno-inline -fno-eliminate-unused-debug-types -fdiagnostics-color=always -fno-common")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} ${COMMON_FLAGS} -g0 -O3")

add_executable(aoc24cpp main.cpp
        day01.cpp
        days.hpp
        day02.cpp
        timing.hpp)
