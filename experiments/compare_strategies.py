from src.simulate import monte_carlo_paths
from src.metrics import summarize
from src.strategies import FlatBet, PercentBet, KellyBet, Martingale

BANKROLL = 1000
ODDS = -110
NUM_BETS = 500
NUM_SIMULATIONS = 1000
MIN_BET = 1


def compare(win_probability: float):
    strategies = {
        "Flat $10": FlatBet(10),
        "2% of bankroll": PercentBet(0.02, MIN_BET),
        "Full Kelly": KellyBet(win_probability, ODDS, 1.0, MIN_BET),
        "Half Kelly": KellyBet(win_probability, ODDS, 0.5, MIN_BET),
        "Martingale $10": Martingale(10),
    }
    print(f"\np(win)={win_probability} at {ODDS}, ${BANKROLL} bankroll, {NUM_BETS} bets x {NUM_SIMULATIONS} sims")
    print(f"{'Strategy':<16}{'Mean':>10}{'Median':>10}{'Profit%':>9}{'Ruin%':>8}{'AvgDD':>8}")
    for name, strategy in strategies.items():
        paths = monte_carlo_paths(BANKROLL, strategy, ODDS, win_probability, NUM_BETS, NUM_SIMULATIONS, seed=42)
        stats = summarize(paths, BANKROLL, MIN_BET)
        print(f"{name:<16}{stats['mean']:>10.0f}{stats['median']:>10.0f}"
              f"{stats['prob_profit']:>9.1%}{stats['risk_of_ruin']:>8.1%}{stats['avg_max_drawdown']:>8.1%}")


if __name__ == "__main__":
    compare(0.50)  # no edge: the sportsbook's cut makes every bet a loser on average
    compare(0.55)  # edge: you win often enough to beat the -110 price
