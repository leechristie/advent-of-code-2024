# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import sys

from day01 import day01 as day01
from day02 import day02 as day02
from day03 import day03 as day03
from day04 import day04 as day04
from day05 import day05 as day05
from day06 import day06 as day06
from day07 import day07 as day07
from day10 import day10 as day10
from day11 import day11 as day11
from day12 import day12 as day12
from day13 import day13 as day13
from day14 import day14 as day14
from day15 import day15 as day15
from day16 import day16 as day16
from day17 import day17 as day17
from day18 import day18 as day18
from day19 import day19 as day19


def main() -> None:

    if len(sys.argv) < 2:
        print('missing argument', file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) > 2:
        print('too many arguments', file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == '1':
        day01()
    elif sys.argv[1] == '2':
        day02()
    elif sys.argv[1] == '3':
        day03()
    elif sys.argv[1] == '4':
        day04()
    elif sys.argv[1] == '5':
        day05()
    elif sys.argv[1] == '6':
        day06()
    elif sys.argv[1] == '7':
        day07()
    elif sys.argv[1] == '10':
        day10()
    elif sys.argv[1] == '11':
        day11()
    elif sys.argv[1] == '12':
        day12()
    elif sys.argv[1] == '13':
        day13()
    elif sys.argv[1] == '14':
        day14()
    elif sys.argv[1] == '15':
        day15()
    elif sys.argv[1] == '16':
        day16()
    elif sys.argv[1] == '17':
        day17()
    elif sys.argv[1] == '18':
        day18()
    elif sys.argv[1] == '19':
        day19()
    else:
        print('invalid day', file=sys.stderr)


if __name__ == "__main__":
    main()
