import json

from playstore_insights import cli, pipeline
from playstore_insights.config import Paths


def test_pipeline_writes_artifacts(tmp_path, monkeypatch):
    paths = Paths()
    monkeypatch.setattr(Paths, "artifacts", property(lambda self: tmp_path))
    result = pipeline.run(paths, compare=False)
    for name in ["rating_model.json", "sentiment_model.json", "metrics.json", "dashboard.json"]:
        assert (tmp_path / name).exists()
    dashboard = json.loads((tmp_path / "dashboard.json").read_text())
    assert dashboard["kpis"]["apps"] == len(result.apps)
    metrics = json.loads((tmp_path / "metrics.json").read_text())
    assert metrics["rating"]["holdout"]["mae"] > 0


def test_cli_rejects_unknown_command(capsys):
    import pytest

    with pytest.raises(SystemExit):
        cli.main(["unknown"])


def test_cli_dispatches(monkeypatch):
    calls = []
    monkeypatch.setattr(pipeline, "run", lambda paths, compare: calls.append(("train", compare)))
    import playstore_insights.site as site

    monkeypatch.setattr(site, "build_site", lambda _, coverage: calls.append(("site", coverage)))
    assert cli.main(["all", "--fast", "--coverage", "88"]) == 0
    assert calls == [("train", False), ("site", 88.0)]
