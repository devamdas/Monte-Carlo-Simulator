import pytest
from src.odds import odds_to_return


def test_positive_odds():
    assert odds_to_return(150) == pytest.approx(2.5)


def test_negative_odds():
    assert odds_to_return(-200) == pytest.approx(1.5)


def test_even_odds():
    assert odds_to_return(100) == pytest.approx(2.0)
    assert odds_to_return(-100) == pytest.approx(2.0)
