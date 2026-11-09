import statistics


def avg_result(results: list) -> float:
    return sum(results) / len(results)


def median_result(results: list) -> float:
    return statistics.median(results)


def std_result(results: list) -> float:
    return statistics.pstdev(results)


def percentile(results: list, p: float) -> float:
    "Linear interpolation between closest ranks, p from 0 to 100"
    ordered = sorted(results)
    k = (len(ordered) - 1) * p / 100
    lower = int(k)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (k - lower)


def prob_profit(results: list, start_bankroll: float) -> float:
    return sum(r > start_bankroll for r in results) / len(results)


def risk_of_ruin(results: list, min_bet: float) -> float:
    "Share of simulations that ended unable to cover the minimum bet"
    return sum(r < min_bet for r in results) / len(results)


def max_drawdown(path: list) -> float:
    "Largest drop from a running peak, as a fraction of that peak"
    peak = path[0]
    worst = 0.0
    for value in path:
        peak = max(peak, value)
        if peak > 0:
            worst = max(worst, (peak - value) / peak)
    return worst


def summarize(paths: list, start_bankroll: float, min_bet: float) -> dict:
    finals = [path[-1] for path in paths]
    return {
        "mean": avg_result(finals),
        "median": median_result(finals),
        "std": std_result(finals),
        "p5": percentile(finals, 5),
        "p95": percentile(finals, 95),
        "prob_profit": prob_profit(finals, start_bankroll),
        "risk_of_ruin": risk_of_ruin(finals, min_bet),
        "avg_max_drawdown": avg_result([max_drawdown(path) for path in paths]),
    }
