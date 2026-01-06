import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from itertools import chain, combinations, repeat
from typing import Iterator, Optional, TextIO

from aocli import solution


@solution(day=10, part=1)
def part_1(raw_input: TextIO) -> int:
    def fewest_presses(
        machine: Machine,
        lights: Optional[tuple[bool, ...]] = None,
        button: int = 0,
    ) -> int:
        lights = lights or tuple(repeat(False, len(machine.lights)))

        if lights == machine.lights:
            return 0
        if button >= len(machine.buttons):
            return sys.maxsize

        skipped = fewest_presses(machine, lights, button + 1)
        next_lights = list(lights)
        for i in machine.buttons[button]:
            next_lights[i] = not lights[i]
        pressed = 1 + fewest_presses(machine, tuple(next_lights), button + 1)

        return min(skipped, pressed)

    return sum(fewest_presses(machine) for machine in parse_machines(raw_input))


@solution(day=10, part=2)
def part_2(raw_input: TextIO) -> int:
    """
    Solution adapted from
    https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/

    Initial attempt was a straightforward O(2^max(B, J)) algorithm where `B` is
    the number of buttons and `J` is the maximum joltage. At each step we'd
    either press the current button (possibly again), or skip it and advance the
    button index until we've either reached the target joltage or otherwise
    considered every possible button. This was super inefficient.

    The linear algebra solutions online did not appeal to me as I neither
    studied that in depth, nor did the solution feel satisfying in any way. This
    one made sense (after a bit) and was fun to catch the "aha" moment of
    realizing why it is correct.
    """

    def solve_bifurcating(machine: Machine) -> int:
        # `button_presses_by_parity` tells us, for a given joltage parity, the
        # button presses which create that parity.
        #
        # Specifically, maps from joltage parity to delta (contribution to
        # joltages) to the minimum number of button presses that achieves that
        # delta/parity. The doubly-nested map structure is an implementation
        # quirk that allows us to make sure that each delta is represented by
        # the *minimum* number of button presses to achieve that delta.
        button_presses_by_parity: defaultdict[
            tuple[int, ...], dict[tuple[int, ...], int]
        ] = defaultdict(dict)
        all_button_combos = chain.from_iterable(
            combinations(machine.buttons, num_buttons)
            for num_buttons in range(len(machine.buttons) + 1)
        )
        for button_combo in all_button_combos:
            delta = [0] * len(machine.joltages)
            for button in button_combo:
                for i in button:
                    delta[i] += 1
            parity = tuple(x % 2 for x in delta)
            if tuple(delta) not in button_presses_by_parity[parity]:
                button_presses_by_parity[parity][tuple(delta)] = len(button_combo)

        @cache
        def min_presses(joltages: tuple[int, ...]) -> int:
            if all(j == 0 for j in joltages):
                return 0

            # Try every button press combination that would even-out the parity. The
            # minimum remaining presses for an even parity joltage state is twice
            # the minimum presses for the joltage state divided in half. This is
            # correct because even parities are created by pressing every button an
            # even number of times. So if there were somehow a more minimal number
            # of presses available (than the minimal presses for half the state),
            # that more minimal number of presses would have to be even per-button
            # as well. Pressing each button one-half of its number of times would
            # create one-half of the current joltage state. Therefore it would
            # itself represent the minimal number of presses to achieve half the
            # current joltage state.
            parity = tuple(j % 2 for j in joltages)
            result = sys.maxsize
            for delta, presses in button_presses_by_parity[parity].items():
                if all(d <= j for d, j in zip(delta, joltages)):
                    next_joltages = tuple((j - d) // 2 for d, j in zip(delta, joltages))
                    result = min(result, presses + 2 * min_presses(next_joltages))

            return result

        return min_presses(tuple(machine.joltages))

    return sum(solve_bifurcating(machine) for machine in parse_machines(raw_input))


@dataclass
class Machine:
    lights: tuple[bool, ...]
    buttons: list[tuple[int, ...]]
    joltages: tuple[int, ...]


def parse_machines(raw_input: TextIO) -> Iterator[Machine]:
    lights_re = r"\[(.+)\]"
    buttons_re = r"\(([\d|\,]+)\)"
    joltages_re = r"{(.+)}"

    for line in raw_input:
        line = line.strip()
        lights = tuple(c == "#" for c in re.findall(lights_re, line)[0])
        buttons = [
            tuple(int(c) for c in s.split(",")) for s in re.findall(buttons_re, line)
        ]
        joltages = tuple(int(c) for c in re.findall(joltages_re, line)[0].split(","))
        yield Machine(lights, buttons, joltages)
