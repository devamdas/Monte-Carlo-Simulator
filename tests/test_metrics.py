import pytest
from src.metrics import (
    avg_result, median_result, percentile, prob_profit, risk_of_ruin, max_drawdown, summarize,
    percentile_path, ruin_curve,
)


def test_avg_and_median():
    assert avg_result([1, 2, 3, 10]) == pytest.approx(4)
    assert median_result([1, 2, 3, 10]) == pytest.approx(2.5)


def test_percentile():
    data = [0, 10, 20, 30, 40]
    assert percentile(data, 0) == 0
    assert percentile(data, 50) == 20
    assert percentile(data, 100) == 40
    assert percentile(data, 25) == pytest.approx(10)


def test_prob_profit_and_ruin():
    finals = [0, 5, 100, 150, 200]
    assert prob_profit(finals, 100) == pytest.approx(0.4)
    assert risk_of_ruin(finals, 10) == pytest.approx(0.4)


def test_max_drawdown():
    assert max_drawdown([100, 120, 60, 90, 130]) == pytest.approx(0.5)
    assert max_drawdown([100, 110, 120]) == 0


def test_summarize_keys():
    stats = summarize([[100, 110], [100, 90]], 100, 10)
    assert stats["mean"] == pytest.approx(100)
    assert stats["prob_profit"] == pytest.approx(0.5)


def test_percentile_path():
    paths = [[100, 110, 120], [100, 90, 80], [100, 100, 100]]
    assert percentile_path(paths, 50) == [100, 100, 100]
    assert percentile_path(paths, 100) == [100, 110, 120]


def test_ruin_curve():
    paths = [[20, 10, 0, 0], [20, 30, 40, 50]]
    assert ruin_curve(paths, 10) == [0, 0, 0.5, 0.5]
