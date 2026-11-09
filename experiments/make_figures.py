from experiments.compare_strategies import run_strategies, BANKROLL, MIN_BET, ODDS
from src.plots import plot_median_paths, plot_ruin_curves, plot_final_distributions

SCENARIOS = {
    "no_edge": 0.50,
    "edge": 0.55,
}

if __name__ == "__main__":
    for label, win_probability in SCENARIOS.items():
        print(f"Simulating {label} (p(win)={win_probability})...")
        results = run_strategies(win_probability)
        setup = f"p(win)={win_probability} at {ODDS}, ${BANKROLL} start"
        plot_median_paths(results, BANKROLL, f"Median bankroll over time · {setup}", f"figures/median_paths_{label}.png")
        plot_ruin_curves(results, MIN_BET, f"Share of simulations gone broke · {setup}", f"figures/ruin_{label}.png")
        plot_final_distributions(results, BANKROLL, f"Final bankroll after 500 bets · {setup}", f"figures/final_distribution_{label}.png")
    print("Saved charts to figures/")
