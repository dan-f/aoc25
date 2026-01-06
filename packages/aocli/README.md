# aocli

CLI orchestration for python solutions to [Advent of Code](https://adventofcode.com/).

## Configuration

A `pyproject.toml` containing a `[tool.aocli]` entry must exist in the invoked directory:

```toml
[tool.aocli]
solutions-pkg = "my_proj.solution" # python package containing solution modules (required)
source-root = "src"                # parent directory of the `solutions-pkg` (optional; default="src")
input-dir = "input"                # directory containing puzzle input files (optional; default="input")
```

## Usage

### Add a solution

Copy the included template with `aocli generate <day>`. This creates a solution module for the given day within the `solutions-pkg` and adds an empty input file to the `input-dir`.

Note that daily solutions must exist as `<solutions-pkg>.day_<day_num>` (e.g. `my_proj.solution.day_1`) and inputs must exist as `<input-dir>/<day_num>.txt` (e.g. `input/1.txt`) in order to be recognized. The names of solution functions do not matter.

### Run a solution

```sh
$ aocli solve <day> <part>
```
