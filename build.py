#!/usr/bin/env python3

import tomli
import tomli_w
import shutil
import subprocess
import sys
from pathlib import Path


root_dir = Path(__file__).parent.resolve()
crate_dir = root_dir / "pngquant"
dist_dir = root_dir / "dist"
cargo_manifest_path = crate_dir / "Cargo.toml"
pyproject_toml_path = root_dir / "pyproject.toml"


def main():
    # maturin expects the 'pyproject.toml' file to be included in the cargo
    # package and located in the same directory as Cargo.toml, so we add it
    # to the package's 'include' list and copy it there.
    cargo_manifest = tomli.load(cargo_manifest_path.open("rb"))
    if (
        "include" in cargo_manifest["package"]
        and "/pyproject.toml" not in cargo_manifest["package"]["include"]
    ):
        cargo_manifest["package"]["include"].append("/pyproject.toml")
        tomli_w.dump(cargo_manifest, cargo_manifest_path.open("wb"))

    shutil.copyfile(pyproject_toml_path, crate_dir / "pyproject.toml")

    try:
        cmd = {
            "sdist": ["maturin", "sdist"],
            "wheel": ["maturin", "build", "--no-sdist", "--release"],
        }[sys.argv[1]]
    except (IndexError, KeyError):
        sys.exit("usage: build.py [sdist|wheel]")

    return subprocess.call(
        cmd + ["-o", str(dist_dir)] + sys.argv[2:], cwd=str(crate_dir)
    )


if __name__ == "__main__":
    sys.exit(main())
