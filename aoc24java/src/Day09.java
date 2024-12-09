// Advent of Code 2024
// Dr Lee A. Christie
//
// GitHub:   @leechristie
// Mastodon: @0x1ac@techhub.social
// Website:  leechristie.com

import java.io.*;
import java.util.*;

public final class Day09 {

    private static List<Integer> parseFilingSystem(String input) {

        char[] data = input.toCharArray();
        final int n = data.length;

        // get the length of each file as an integer
        int[] lengths;
        lengths = new int[n];
        for (int i = 0; i < n; i++) {
            lengths[i] = Integer.parseInt("" + data[i]);
        }

        // get the id of each file an integer
        List<Integer> rv = new ArrayList<>();
        boolean inFile = false;
        int id = -1;
        for (int length : lengths) {
            inFile = !inFile;
            if (inFile) {
                id++;
            }
            if (inFile) {
                if (length == 0) {
                    throw new AssertionError("zero length file");
                }
            }
            for (int i = 0; i < length; i++) {
                if (inFile) {
                    rv.add(id);
                } else {
                    rv.add(-1);
                }
            }
        }

        return rv;

    }

    private static int firstFreeSpace(List<Integer> filingSystem) {
        int rv = 0;
        while (filingSystem.get(rv) != -1) {
            rv++;
        }
        return rv;
    }

    private static int nextFreeSpace(List<Integer> filingSystem, int rv) {
        while (filingSystem.get(rv) != -1) {
            rv++;
        }
        return rv;
    }

    private static int previousFileSpace(List<Integer> filingSystem, int rv) {
        while (filingSystem.get(rv) == -1) {
            rv--;
        }
        return rv;
    }

    private static void compact_method1(List<Integer> fs) {
        int freeSpacePointer = firstFreeSpace(fs);
        int endPointer = fs.size() - 1;
        while (freeSpacePointer < endPointer) {
            fs.set(freeSpacePointer, fs.get(endPointer));
            fs.set(endPointer, -1);
            freeSpacePointer = nextFreeSpace(fs, freeSpacePointer);
            endPointer = previousFileSpace(fs, endPointer);
        }
    }

    private static void compact_method2_no_hole_opt(List<Integer> fs) {

        int endPointer = fs.size() - 1;
        int endLength = endLength(fs, endPointer);

        while (endPointer >= 0) {

            int currentBlockId = fs.get(endPointer);

            int destinationIndex = firstSuitableHoleNoOpt(fs, endPointer, endLength);
            if (destinationIndex != -1)
                moveData(fs, endPointer, endLength, destinationIndex);

            while (fs.get(endPointer) == currentBlockId || fs.get(endPointer) == -1) {
                endPointer--;
                if (endPointer < 0)
                    return;
            }
            endLength = endLength(fs, endPointer);

        }

    }

    private static void moveData(List<Integer> fs, int endPointer, int endLength, int holeIndex) {
        int expectedValue = fs.get(endPointer);
        assert expectedValue >= 0;
        for (int i = 0; i < endLength; i++) {
            int value = fs.get(endPointer - i);
            assert value == expectedValue;
            assert fs.get(endPointer - i) == value;
            assert fs.get(holeIndex + i) == -1;
            fs.set(endPointer - i, -1);
            fs.set(holeIndex + i, value);
            assert fs.get(endPointer - i) == -1;
            assert fs.get(holeIndex + i) == value;
        }
    }

    private static int firstSuitableHoleNoOpt(List<Integer> fs, int endPointer, int endLength) {
        int rv = 0;
        while (rv < endPointer) {
            if (fs.get(rv) == -1) {
                if (holeLength(fs, rv) >= endLength) {
                    return rv;
                } else {
                    rv++;
                }
            } else {
                rv++;
            }
        }
        return -1;
    }

    private static int holeLength(List<Integer> fs, int start) {
        assert fs.get(start) == -1;
        int rv = 0;
        while (fs.get(start) == -1) {
            rv++;
            start++;
        }
        return rv;
    }

    private static int endLength(List<Integer> fs, int endPointer) {
        int value = fs.get(endPointer);
        assert value != -1;
        int rv = 0;
        while (endPointer >= 0 && fs.get(endPointer) == value) {
            rv++;
            endPointer--;
        }
        return rv;
    }

    private static int freeSpaceLength(List<Integer> fs, int freeSpacePointer) {
        assert fs.get(freeSpacePointer) == -1;
        int rv = 0;
        while (fs.get(freeSpacePointer) == -1) {
            rv++;
            freeSpacePointer++;
        }
        return rv;
    }

    private static void printLengths(int endPointer, int endLength, PrintStream out) {
        out.println("       ".repeat(endPointer) + " " + endLength);
    }

    private static long checksum(List<Integer> filingSystem) {
        long rv = 0;
        int value;
        for (int i = 0; i < filingSystem.size(); i++) {
            value = filingSystem.get(i);
            if (value > -1) {
                rv += (long) i * (long) value;
            }
            assert rv >= 0;
        }
        return rv;
    }

    public static void solve() throws IOException {

        final long start = System.nanoTime();

        // load two copies of the data for Part 1 and Part 2
        List<Integer> filingSystem;
        try (final BufferedReader in = new BufferedReader(new FileReader(new File("input09.txt")))) {
            filingSystem = parseFilingSystem(in.readLine());
        }
        List<Integer> filingSystemCopy = new ArrayList<>(filingSystem);

        // solve part 1
        compact_method1(filingSystem);
        long part1 = checksum(filingSystem);

        // solve part 2
        compact_method2_no_hole_opt(filingSystemCopy);
        long part2 = checksum(filingSystemCopy);

        double time = (System.nanoTime() - start) * 1e-9;
        System.out.println("Advent of Code 2024");
        System.out.println("Day 9 - Disk Fragmenter");
        System.out.printf("Part 1: %d\n", part1);
        assert 6307275788409L == part1;
        System.out.printf("Part 2: %d\n", part2);
        assert 6327174563252L == part2;
        System.out.printf("Time Taken: %.6f s\n", time);

    }

}
