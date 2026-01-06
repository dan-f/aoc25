import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = ["Config", "load_config"]


def load_config(project_root: Path) -> Config:
    source_root = project_root.joinpath("src")
    input_dir = project_root.joinpath("input")

    with project_root.joinpath("pyproject.toml").open("rb") as f:
        config_data = tomllib.load(f)

    if (tool := config_data.get("tool")) and (aocli := tool.get("aocli")):
        if data := aocli.get("source-root"):
            source_root = data
        if data := aocli.get("input-dir"):
            input_dir = parse_path(data)
        solutions_pkg = parse_str(aocli.get("solutions-pkg"))

    return Config(source_root, solutions_pkg, input_dir)


@dataclass
class Config:
    source_root: Path
    solutions_pkg: str
    input_dir: Path


def parse_path(data: Any) -> Path:
    try:
        return Path(data)
    except TypeError as e:
        raise TypeError(f"Expected path, got: {data}") from e


def parse_str(data: Any) -> str:
    if type(data) is str:
        return data
    raise TypeError(f"Expected string, got: {data}")
