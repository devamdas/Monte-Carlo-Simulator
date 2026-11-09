import pytest
from src.strategies import FlatBet, PercentBet, KellyBet, Martingale, kelly_fraction
from src.simulate import simulate_seq


def test_flat_and_percent():
    assert FlatBet(10).bet_size(500) == 10
    assert PercentBet(0.02).bet_size(500) == pytest.approx(10)
    assert PercentBet(0.02, min_bet=1).bet_size(10) == 1


def test_kelly_fraction():
    # even money (+100) with 60% win chance: f = (1*0.6 - 0.4) / 1 = 0.2
    assert kelly_fraction(0.6, 100) == pytest.approx(0.2)
    # no edge at -110 with 50%: never bet
    assert kelly_fraction(0.5, -110) == 0
    assert KellyBet(0.5, -110).bet_size(1000) == 0


def test_martingale_doubles_and_resets():
    m = Martingale(10)
    m.record(False)
    m.record(False)
    assert m.bet_size(1000) == 40
    m.record(True)
    assert m.bet_size(1000) == 10
    assert Martingale(10).bet_size(5) == 5


def test_martingale_busts_on_losing_streak():
    # always loses: bets 10, 20, 40, then all-in on the last 30
    path = simulate_seq(100, Martingale(10), -110, 0.0, 10)
    assert path[:5] == [100, 90, 70, 30, 0]


def test_kelly_skips_without_edge():
    path = simulate_seq(1000, KellyBet(0.5, -110), -110, 0.5, 20)
    assert all(value == 1000 for value in path)
