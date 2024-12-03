# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import sys

from day01 import day01 as day01
from day02 import day02 as day02


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


if __name__ == "__main__":
    main()