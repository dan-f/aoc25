import sys
from aoc.cli import parser


def main():
    parsed = parser.parse_args(sys.argv[1:])
    print(f"day: {parsed.day}")
    print(f"part: {parsed.part}")


if __name__ == "__main__":
    main()
