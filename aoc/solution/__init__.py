import shutil
from pathlib import Path


def write_template(day: int, input_dir: Path) -> None:
    solns_dir = Path(__file__).parent
    soln_template_path = solns_dir.joinpath("_template.py")
    soln_path = solns_dir.joinpath(f"day_{day}.py")
    if soln_path.exists():
        raise FileExistsError(f"solution file for day {day} already exists")

    if not input_dir.exists():
        input_dir.mkdir()
    input_path = input_dir.joinpath(f"{day}.txt")
    if not input_path.exists():
        input_path.touch()

    shutil.copyfile(soln_template_path.resolve(), soln_path.resolve())
    print(f"Day {day} solution file: {soln_path}")
    print(f"Day {day} input file: {input_path}")
