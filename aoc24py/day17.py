# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com

import itertools
import time
from typing import TextIO, Optional
from enum import Enum
import tqdm.auto as tqdm


class Machine:

    __slots__ = ['a', 'b', 'c', 'prog', 'ic', 'length']

    def __init__(self, register_a: int, register_b: int, register_c: int, program: tuple[int, ...], instruction_counter: int=0) -> None:
        assert len(program) % 2 == 0
        self.a = register_a
        self.b = register_b
        self.c = register_c
        self.prog = program
        self.ic = instruction_counter
        self.length = len(self.prog) // 2

    def _evaluate_operand(self, operand: int) -> Optional[int]:
        assert (0 <= operand <= 7), f'invalid operand {operand}'
        if operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        assert operand == 7
        return None  # operand 7 is not a combo operator

    def evaluate_operand(self) -> tuple[int, Optional[int]]:
        operand: int = self.prog[self.ic + 1]
        return operand, self._evaluate_operand(operand)

    def __len__(self):
        return self.length

    def __iter__(self):
        return self

    def __next__(self) -> tuple['OpCode', int, int]:
        if self.ic >= len(self.prog):
            raise StopIteration
        opcode: 'OpCode' = self.evaluate_opcode()
        literal, combo = self.evaluate_operand()
        self.ic += 2
        return opcode, literal, combo

    def evaluate_opcode(self) -> 'OpCode':
        opcode: int = self.prog[self.ic]
        return OpCode.lookup(opcode)

    def reinitialize(self, register_a: int) -> None:
        self.a = register_a
        self.b = 0
        self.c = 0
        self.ic = 0

    def execute(self, opcode: 'OpCode', literal: int, combo: Optional[int], output: list[int], expected: Optional[tuple[int, ...]]=None) -> bool:

        # The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The
        # denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would
        # divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated
        # to an integer and then written to the A register.
        if opcode == OpCode.ADV:
            assert combo is not None
            self.a = self.a >> combo

        # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand,
        # then stores the result in register B.
        elif opcode == OpCode.BXL:
            self.b ^= literal % 8

        # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its
        # lowest 3 bits), then writes that value to the B register.
        elif opcode == OpCode.BST:
            assert combo is not None
            self.b = combo % 8

        # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
        # it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps,
        # the instruction pointer is not increased by 2 after this instruction.
        elif opcode == OpCode.JNZ:
            if self.a != 0:
                self.ic = literal

        # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result
        # in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        elif opcode == OpCode.BXC:
            self.b = (self.b ^ self.c) % 8

        # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
        # (If a program outputs multiple values, they are separated by commas.)
        elif opcode == OpCode.OUT:
            assert combo is not None
            output.append(combo % 8)
            if expected is not None and len(output) > len(expected):
                return True  # output grew too long
            index = len(output) - 1
            if expected is not None and output[index] != expected[index]:
                return True  # output adding wrong value

        # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the
        # B register. (The numerator is still read from the A register.)
        elif opcode == OpCode.BDV:
            assert combo is not None
            self.b = self.a >> combo

        # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the
        # C register. (The numerator is still read from the A register.)
        elif opcode == OpCode.CDV:
            assert combo is not None
            self.c = self.a >> combo

        else:
            raise ValueError('Unable to execute!')

        return False

    def __str__(self):
        return f'Machine[a={self.a}, b={self.b}, c={self.c}, ic={self.ic}, prog={self.prog}]'

    def __repr__(self):
        if self.ic == 0:
            return f'Machine(register_a={self.a}, register_b={self.b}, register_c={self.c}, program={self.prog}]'
        else:
            return f'Machine(register_a={self.a}, register_b={self.b}, register_c={self.c}, program={self.prog}, instruction_counter={self.ic}]'

    def run(self) -> str:
        output: list[int] = []
        for opcode, literal, combo in self:
            self.execute(opcode, literal, combo, output)
        return ','.join([str(value) for value in output])

    def expect(self, output_buffer: list[int], expected: tuple[int, ...]) -> bool:
        output_buffer.clear()
        for opcode, literal, combo in self:
            if self.execute(opcode, literal, combo, output_buffer, expected):
                return False
        return len(expected) == len(output_buffer)

    def mine(self) -> int:
        buffer: list[int] = []
        for register_a in tqdm.tqdm(itertools.count()):
            self.reinitialize(register_a)
            if self.expect(buffer, self.prog):
                return register_a


class OpCode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

    @staticmethod
    def lookup(opcode: int) -> 'OpCode':
        assert 0 <= opcode <= 7
        if opcode == 0:
            return OpCode.ADV
        if opcode == 1:
            return OpCode.BXL
        if opcode == 2:
            return OpCode.BST
        if opcode == 3:
            return OpCode.JNZ
        if opcode == 4:
            return OpCode.BXC
        if opcode == 5:
            return OpCode.OUT
        if opcode == 6:
            return OpCode.BDV
        assert opcode == 7
        return OpCode.CDV


def read_register(file: TextIO, register_id: str) -> int:
    line: str = next(file)
    prefix: str = f'Register {register_id}: '
    assert line.startswith(prefix)
    line = line.removeprefix(prefix)
    return int(line)


def read_program(file: TextIO) -> tuple[int, ...]:
    line: str = next(file)
    prefix: str = 'Program: '
    assert line.startswith(prefix)
    line = line.removeprefix(prefix)
    numbers: tuple[int, ...] = tuple(int(number) for number in line.split(','))
    return numbers


def read_input(filename: str) -> Machine:
    with open(filename) as file:
        register_a = read_register(file, 'A')
        register_b = read_register(file, 'B')
        register_c = read_register(file, 'C')
        assert not next(file).strip()
        program = read_program(file)
        for line in file:
            line = line.strip()
            print(line)
        return Machine(register_a, register_b, register_c, program)

def day17() -> None:

    start: float = time.perf_counter()

    # machine: Machine = read_input('small17.txt')
    # machine: Machine = read_input('example17.txt')
    machine: Machine = read_input('input17.txt')

    part1: str = machine.run()
    part2: int = machine.mine()

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 17 - Chronospatial Computer")
    print(f"Part 1: {part1}")
    assert part1 in ('5,7,3,0', '4,6,3,5,6,3,5,2,1,0', '4,6,1,4,2,1,3,1,6')
    print(f"Part 2: {part2}")
    if part1 == '5,7,3,0':
        assert part2 == 117440
    # 118,393,894,510 is too low!
    print(f"Time Taken: {stop-start:.6f} s")
