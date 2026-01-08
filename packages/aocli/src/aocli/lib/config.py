import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

__all__ = ["Config", "load_config"]


def load_config(project_root: Path) -> Config:
    with project_root.joinpath("pyproject.toml").open("rb") as f:
        config_data = tomllib.load(f)

    conf = (tool := config_data.get("tool", {})) and tool.get("aocli")

    return Config(
        source_root=conf.get("source-root", project_root.joinpath("src")),
        solutions_pkg=parse_str(conf.get("solutions-pkg")),
        input_dir=(
            (data := conf.get("input-dir"))
            and parse_path(data)
            or project_root.joinpath("input")
        ),
        year=conf.get("year"),
        session_cookie=os.getenv("AOC_SESSION_COOKIE"),
    )


@dataclass
class Config:
    source_root: Path
    solutions_pkg: str
    input_dir: Path
    year: Optional[int]
    session_cookie: Optional[str]


def parse_path(data: Any) -> Path:
    try:
        return Path(data)
    except TypeError as e:
        raise TypeError(f"Expected path, got: {data}") from e


def parse_str(data: Any) -> str:
    if type(data) is str:
        return data
    raise TypeError(f"Expected string, got: {data}")
