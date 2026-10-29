from playstore_insights import analytics


def test_kpis(apps, reviews):
    k = analytics.kpis(apps, reviews)
    assert k["apps"] == len(apps)
    assert 0 < k["free_share"] < 1 and 0 < k["positive_share"] < 1
    assert 3.5 < k["avg_rating"] < 4.5


def test_category_stats(apps):
    stats = analytics.category_stats(apps)
    assert stats["apps"].sum() == len(apps)
    assert stats["apps"].is_monotonic_decreasing


def test_distributions(apps):
    dist = analytics.rating_distribution(apps)
    assert sum(dist["counts"]) == apps["rating"].notna().sum()
    tiers = analytics.installs_tiers(apps)
    assert sum(tiers["apps"]) == len(apps)
    years = analytics.updates_by_year(apps)
    assert sum(years["apps"]) == len(apps)


def test_correlation_is_symmetric(apps):
    corr = analytics.correlation(apps)
    m = corr["matrix"]
    assert all(m[i][j] == m[j][i] for i in range(len(m)) for j in range(len(m)))


def test_misc_views(apps, reviews):
    assert len(analytics.top_apps(apps, n=5)) == 5
    assert {row["type"] for row in analytics.free_vs_paid(apps)} == {"Free", "Paid"}
    assert analytics.content_rating_breakdown(apps)[0]["label"] == "Everyone"
    assert len(analytics.scatter_sample(apps, n=50)) == 50
    sent = analytics.sentiment_by_category(apps, reviews)
    assert set(sent["series"]) == {"Positive", "Neutral", "Negative"}
    pol = analytics.polarity_vs_rating(apps, reviews)
    assert -1 <= pol["spearman"] <= 1 and pol["points"]
