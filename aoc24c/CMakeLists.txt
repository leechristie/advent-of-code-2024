cmake_minimum_required(VERSION 3.29)
project(aoc24c C)

set(CMAKE_C_STANDARD 23)

set(COMMON_FLAGS "${COMMON_FLAGS} -Wall -Wno-unused-function -Wextra -Wpedantic -Werror")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} ${COMMON_FLAGS} -g3 -O0 -fsanitize=address,undefined -fno-omit-frame-pointer -fstack-protector-strong -fno-inline -fno-eliminate-unused-debug-types -fdiagnostics-color=always -fno-common")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} ${COMMON_FLAGS} -g0 -O3")

add_executable(aoc24c main.c
        day01.c
        days.h
        list.h
        io.h
        fatal.h
        day02.c
        timing.h
        day03.c
        day04.c
        strings.h
        points.h
        grid.h)
