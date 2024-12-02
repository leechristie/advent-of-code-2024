# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import sys
import numpy as np
from decimal import Decimal


def main() -> None:
    total = Decimal("0")
    samples = []
    count = 0
    assert len(sys.argv) == 2
    with open(sys.argv[-1]) as file:
        for line in file:
            line = line.strip()
            if line.startswith('Time Taken: ') and line.endswith(' s'):
                line = line.removeprefix('Time Taken: ')
                line = line.removesuffix(' s')
                assert len(line.split('.')) == 2
                assert len(line.split('.')[-1]) == 6
                total += Decimal(line)
                count += 1
                samples.append(np.float64(Decimal(line)))
    print()
    print("Samples Found:", count)
    print(f"Mean: {total / count:.6f}")
    print(f"Standard Deviation: {float(round(np.std(samples, ddof=1), 6)):.6f}")


if __name__ == '__main__':
    main()
