"""Project paths and global constants."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _default_root() -> Path:
    source_root = Path(__file__).resolve().parents[2]
    return source_root if (source_root / "data").is_dir() else Path.cwd()


ROOT = Path(os.environ.get("PLAYSTORE_ROOT") or _default_root())
RANDOM_STATE = 42
REFERENCE_DATE = "2018-08-08"


@dataclass(frozen=True)
class Paths:
    root: Path = ROOT

    @property
    def raw_apps(self) -> Path:
        return self.root / "data" / "raw" / "googleplaystore.csv"

    @property
    def raw_reviews(self) -> Path:
        return self.root / "data" / "raw" / "googleplaystore_user_reviews.csv"

    @property
    def artifacts(self) -> Path:
        return self.root / "artifacts"

    @property
    def web(self) -> Path:
        return self.root / "web"

    @property
    def site(self) -> Path:
        return self.root / "build" / "site"


PATHS = Paths()
