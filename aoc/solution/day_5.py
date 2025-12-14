from io import TextIOWrapper


def part_1(raw_input: TextIOWrapper) -> int:
    ranges, ids = parse_input(raw_input)
    merged = merge_ranges(ranges)

    def is_fresh(id_: int) -> bool:
        lo = 0
        hi = len(merged)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if merged[mid][0] <= id_ <= merged[mid][1]:
                return True
            elif id_ < merged[mid][0]:
                hi = mid
            elif id_ > merged[mid][1]:
                lo = mid + 1
        return False

    fresh_ids = sum(1 for id_ in ids if is_fresh(id_))
    return fresh_ids


def part_2(raw_input: TextIOWrapper) -> int:
    ranges, _ = parse_input(raw_input)
    return sum(r[1] - r[0] + 1 for r in merge_ranges(ranges))


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges.sort(key=lambda r: r[0])
    merged = [list(ranges[0])]
    for i in range(1, len(ranges)):
        if merged[-1][0] <= ranges[i][0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], ranges[i][1])
        else:
            merged.append(list(ranges[i]))
    return [(r[0], r[1]) for r in merged]


def parse_input(raw_input: TextIOWrapper) -> tuple[list[tuple[int, int]], list[int]]:
    def parse_range(r: str) -> tuple[int, int]:
        [start, stop] = r.split("-")
        return int(start), int(stop)

    [ranges_str, ids_str] = raw_input.read().strip().split("\n\n")

    return (
        [parse_range(r) for r in ranges_str.split("\n")],
        [int(id_) for id_ in ids_str.split("\n")],
    )
