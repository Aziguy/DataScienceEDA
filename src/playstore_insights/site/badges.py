"""shields.io endpoint badges published alongside the site."""

from __future__ import annotations


def badge(label: str, message: str, color: str) -> dict:
    return {"schemaVersion": 1, "label": label, "message": message, "color": color}


def coverage_color(percent: float) -> str:
    if percent >= 90:
        return "brightgreen"
    if percent >= 75:
        return "green"
    if percent >= 60:
        return "yellow"
    return "red"


def score_color(score: float) -> str:
    return coverage_color(score * 100)
