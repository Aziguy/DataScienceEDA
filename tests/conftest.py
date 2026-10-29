from pathlib import Path

import pytest

from playstore_insights.data import clean_apps, clean_reviews, load_apps, load_reviews

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def raw_apps():
    return load_apps()


@pytest.fixture(scope="session")
def apps(raw_apps):
    return clean_apps(raw_apps)[0]


@pytest.fixture(scope="session")
def reviews():
    return clean_reviews(load_reviews())


@pytest.fixture
def tiny_raw():
    return load_apps(FIXTURES / "apps.csv")
