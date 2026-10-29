"""Smoke tests: every Streamlit view renders without exception."""

from pathlib import Path

import pytest

pytest.importorskip("streamlit")
pytest.importorskip("plotly")
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app"


@pytest.mark.parametrize("view", ["overview", "explore", "sentiment", "predict", "profiling"])
def test_view_renders(view, monkeypatch):
    monkeypatch.syspath_prepend(str(APP))
    at = AppTest.from_file(str(APP / "views" / f"{view}.py"), default_timeout=120)
    at.run()
    assert not at.exception, at.exception
