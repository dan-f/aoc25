from pathlib import Path
from urllib import request

from aocli.lib.config import Config

__all__ = ["write_input_file"]


def write_input_file(day: int, config: Config) -> tuple[bool, Path]:
    if not config.input_dir.exists():
        config.input_dir.mkdir()
    input_path = config.input_dir.joinpath(f"{day}.txt")

    if input_path.exists():
        return False, input_path

    if config.year is not None and config.session_cookie is not None:
        req = request.Request(f"https://adventofcode.com/{config.year}/day/{day}/input")
        req.add_header("Cookie", f"session={config.session_cookie}")
        with request.urlopen(req) as rsp:
            with input_path.open("wb") as input_file:
                input_file.write(rsp.read())
    else:
        input_path.touch()
    return True, input_path
