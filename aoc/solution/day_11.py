from collections import defaultdict
from functools import cache
from io import TextIOWrapper


def part_1(raw_input: TextIOWrapper) -> int:
    devices = parse_devices(raw_input)

    def paths(cur: str, target: str) -> int:
        if cur == target:
            return 1
        outs = devices[cur]
        if not outs:
            return 0

        return sum(paths(out, target) for out in outs)

    return paths("you", "out")


def part_2(raw_input: TextIOWrapper) -> int:
    devices = parse_devices(raw_input)

    @cache
    def paths(cur: str, target: str, dac: bool = False, fft: bool = False) -> int:
        if cur == target:
            return 1 if dac and fft else 0
        outs = devices[cur]
        if not outs:
            return 0

        dac = dac or cur == "dac"
        fft = fft or cur == "fft"

        return sum(paths(out, target, dac, fft) for out in outs)

    return paths("svr", "out")


def parse_devices(raw_input: TextIOWrapper) -> defaultdict[str, list[str]]:
    result = defaultdict[str, list[str]](list)

    for line in raw_input:
        [key, neighbors] = line.strip().split(":")
        result[key].extend([n for n in neighbors.strip().split(" ")])

    return result
