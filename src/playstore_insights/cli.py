"""Command line entry point: `playstore-insights {train,site,all}`."""

from __future__ import annotations

import argparse
import logging

from . import pipeline
from .config import PATHS


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="playstore-insights")
    parser.add_argument("command", choices=["train", "site", "all"])
    parser.add_argument("--fast", action="store_true", help="skip cross-validated comparison")
    parser.add_argument("--coverage", type=float, help="coverage percent for the site badge")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if args.command in {"train", "all"}:
        pipeline.run(PATHS, compare=not args.fast)
    if args.command in {"site", "all"}:
        from .site import build_site

        build_site(PATHS, coverage=args.coverage)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
