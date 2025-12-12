import sys

from aoc.cli import parser
from aoc.runner import run


def main():
    args = parser.parse_args(sys.argv[1:])
    result = run(args.day, args.part)
    print(f"Day {args.day} part {args.part} result: {result}")


if __name__ == "__main__":
    main()
