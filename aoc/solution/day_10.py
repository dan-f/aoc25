import re
import sys
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Iterator, Optional


def part_1(raw_input: TextIOWrapper) -> int:
    def fewest_presses(
        machine: Machine,
        lights: Optional[list[bool]] = None,
        button: int = 0,
    ) -> int:
        lights = lights or [False] * len(machine.lights)

        if lights == machine.lights:
            return 0
        if button >= len(machine.buttons):
            return sys.maxsize

        skipped = fewest_presses(machine, lights, button + 1)
        for i in machine.buttons[button]:
            lights[i] = not lights[i]
        pressed = 1 + fewest_presses(machine, lights, button + 1)
        for i in machine.buttons[button]:
            lights[i] = not lights[i]

        return min(skipped, pressed)

    return sum(fewest_presses(machine) for machine in parse_machines(raw_input))


def part_2(raw_input: TextIOWrapper) -> int:
    def fewest_presses(
        machine: Machine, joltages: Optional[list[int]] = None, button: int = 0
    ) -> int:
        joltages = joltages or [0] * len(machine.joltages)

        if joltages == machine.joltages:
            return 0
        if any(current > target for current, target in zip(joltages, machine.joltages)):
            return sys.maxsize
        if button >= len(machine.buttons):
            return sys.maxsize

        skipped = fewest_presses(machine, joltages, button + 1)
        for i in machine.buttons[button]:
            joltages[i] += 1
        pressed = 1 + fewest_presses(machine, joltages, button)
        for i in machine.buttons[button]:
            joltages[i] -= 1

        return min(skipped, pressed)

    return sum(fewest_presses(machine) for machine in parse_machines(raw_input))


@dataclass
class Machine:
    lights: list[bool]
    buttons: list[list[int]]
    joltages: list[int]


def parse_machines(raw_input: TextIOWrapper) -> Iterator[Machine]:
    lights_re = r"\[(.+)\]"
    buttons_re = r"\(([\d|\,]+)\)"
    joltages_re = r"{(.+)}"

    for line in raw_input:
        line = line.strip()
        lights = [c == "#" for c in re.findall(lights_re, line)[0]]
        buttons = [[int(c) for c in s.split(",")] for s in re.findall(buttons_re, line)]
        joltages = [int(c) for c in re.findall(joltages_re, line)[0].split(",")]
        yield Machine(lights, buttons, joltages)
