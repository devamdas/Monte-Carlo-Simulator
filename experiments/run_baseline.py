from src.simulate import monte_carlo_paths
from src.metrics import summarize


def report(name: str, bankroll: float, bet: float, odds: float, win_probability: float, num_bets: int, num_simulations: int):
    paths = monte_carlo_paths(bankroll, bet, odds, win_probability, num_bets, num_simulations, seed=42)
    stats = summarize(paths, bankroll, bet)
    print(f"\n{name}: ${bankroll} bankroll, ${bet} bets at {odds}, p(win)={win_probability}, {num_bets} bets x {num_simulations} sims")
    print(f"  Mean final bankroll:   ${stats['mean']:.2f}")
    print(f"  Median final bankroll: ${stats['median']:.2f}")
    print(f"  Std deviation:         ${stats['std']:.2f}")
    print(f"  5th-95th percentile:   ${stats['p5']:.2f} to ${stats['p95']:.2f}")
    print(f"  Chance of profit:      {stats['prob_profit']:.1%}")
    print(f"  Risk of ruin:          {stats['risk_of_ruin']:.1%}")
    print(f"  Avg max drawdown:      {stats['avg_max_drawdown']:.1%}")


print("Running Monte Carlo simulations...")
report("Baseline", bankroll=1000, bet=10, odds=-110, win_probability=0.5, num_bets=100, num_simulations=1000)
report("Small bankroll", bankroll=100, bet=10, odds=-110, win_probability=0.5, num_bets=500, num_simulations=1000)
