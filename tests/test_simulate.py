import pytest
from src.simulate import simulate_bet, simulate_seq, monte_carlo_simulation


def test_win_adds_profit_only():
    # win_probability=1 always wins; -110 pays 100/110 of the stake
    assert simulate_bet(1000, 110, -110, 1.0) == pytest.approx(1100)


def test_loss_subtracts_bet():
    assert simulate_bet(1000, 10, -110, 0.0) == pytest.approx(990)


def test_same_seed_same_results():
    a = monte_carlo_simulation(1000, 10, -110, 0.5, 50, 20, seed=1)
    b = monte_carlo_simulation(1000, 10, -110, 0.5, 50, 20, seed=1)
    assert a == b


def test_average_matches_expected_value():
    # EV per bet at -110, p=0.5: 0.5 * (100/110) * 10 - 0.5 * 10
    ev_per_bet = 0.5 * (100 / 110) * 10 - 0.5 * 10
    results = monte_carlo_simulation(1000, 10, -110, 0.5, 100, 5000, seed=0)
    assert sum(results) / len(results) == pytest.approx(1000 + 100 * ev_per_bet, abs=3)


def test_path_length_and_start():
    path = simulate_seq(1000, 10, -110, 0.5, 25)
    assert len(path) == 26
    assert path[0] == 1000


def test_stops_when_broke():
    # always loses: 3 bets of $10 drain $30, then betting stops
    path = simulate_seq(30, 10, -110, 0.0, 10)
    assert path[:4] == [30, 20, 10, 0]
    assert all(value == 0 for value in path[3:])
    assert min(path) >= 0
