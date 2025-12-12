import sys

from aoc import cli, runner, solution


def main():
    args = cli.parser.parse_args(sys.argv[1:])
    match args.command:
        case "run":
            result = runner.run(args.day, args.part)
            print(f"Day {args.day} part {args.part} result: {result}")
        case "gen":
            solution.write_template(args.day)
        case _:
            cli.parser.print_help()


if __name__ == "__main__":
    main()
