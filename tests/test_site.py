import json
import shutil

import pytest

from playstore_insights.config import PATHS, Paths
from playstore_insights.site import build_site
from playstore_insights.site.badges import coverage_color, score_color


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    artifacts = tmp_path / "artifacts"
    site = tmp_path / "site"
    if PATHS.artifacts.exists():
        shutil.copytree(PATHS.artifacts, artifacts)
    monkeypatch.setattr(Paths, "artifacts", property(lambda self: artifacts))
    monkeypatch.setattr(Paths, "site", property(lambda self: site))
    return Paths()


def test_build_site(isolated):
    out = build_site(isolated, coverage=93.4)
    for page in ["index", "explore", "sentiment", "model", "about"]:
        assert (out / f"{page}.html").exists()
    for name in ["apps", "dashboard", "metrics", "rating_model", "sentiment_model", "meta"]:
        assert (out / "data" / f"{name}.json").exists()
    apps = json.loads((out / "data" / "apps.json").read_text())
    assert apps["columns"][0] == "app" and len(apps["rows"]) > 9000
    badge = json.loads((out / "badges" / "coverage.json").read_text())
    assert badge["message"] == "93%" and badge["color"] == "brightgreen"
    assert (out / ".nojekyll").exists()
    assert build_site(isolated) == out


@pytest.mark.parametrize(
    ("value", "color"), [(95, "brightgreen"), (80, "green"), (65, "yellow"), (10, "red")]
)
def test_badge_colors(value, color):
    assert coverage_color(value) == color
    assert score_color(value / 100) == color
