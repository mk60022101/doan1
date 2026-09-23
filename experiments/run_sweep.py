"""Run reproducible parameter sweeps with checkpoint and resume support."""

import argparse
from pathlib import Path


def run_sweep(config: dict, output_dir: Path, seed: int = 0, resume: bool = True):
    """Run a sweep and persist progress so interrupted runs can resume."""
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()
    raise NotImplementedError("Connect CLI arguments to the sweep implementation.")


if __name__ == "__main__":
    main()
