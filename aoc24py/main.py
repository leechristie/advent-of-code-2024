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
    else:
        print('invalid day', file=sys.stderr)


if __name__ == "__main__":
    main()
