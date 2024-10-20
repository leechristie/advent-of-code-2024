cmake_minimum_required(VERSION 3.29)
project(aoc24c C)

set(CMAKE_C_STANDARD 23)

set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} ${COMMON_FLAGS} -g3 -O0 -fsanitize=address,undefined -fno-omit-frame-pointer -fstack-protector-strong -fno-inline -fno-eliminate-unused-debug-types -fdiagnostics-color=always -fno-common")

add_executable(aoc24c main.c)
