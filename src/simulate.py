import random
from src.odds import odds_to_return
from src.strategies import FlatBet

def simulate_bet(bankroll: float, bet: float, odds: float, win_probability: float, rng=random) -> float:
    if rng.random() < win_probability:
        profit = bet * (odds_to_return(odds) - 1)
        return bankroll + profit
    else:
        return bankroll - bet
def simulate_seq(bankroll: float, strategy, odds: float, win_probability: float, num_bets: int, rng=random) -> list:
    "Returns the bankroll after every bet, starting with the initial bankroll"
    "strategy can be a strategy object or a number (treated as a flat bet)"
    "Stops betting once the bankroll can't cover the bet; the rest of the path stays flat"
    if not hasattr(strategy, "bet_size"):
        strategy = FlatBet(strategy)
    strategy.reset()
    path = [bankroll]
    for _ in range(num_bets):
        bet = strategy.bet_size(bankroll)
        if 0 < bet <= bankroll:
            new_bankroll = simulate_bet(bankroll, bet, odds, win_probability, rng)
            strategy.record(new_bankroll > bankroll)
            bankroll = new_bankroll
        path.append(bankroll)
    return path
def monte_carlo_paths(bankroll: float, strategy, odds: float, win_probability: float, num_bets: int, num_simulations: int, seed=None) -> list:
    rng = random.Random(seed)
    paths = []
    for _ in range(num_simulations):
        paths.append(simulate_seq(bankroll, strategy, odds, win_probability, num_bets, rng))
    return paths
def monte_carlo_simulation(bankroll: float, strategy, odds: float, win_probability: float, num_bets: int, num_simulations: int, seed=None) -> list:
    "Returns only the final bankroll of each simulation"
    paths = monte_carlo_paths(bankroll, strategy, odds, win_probability, num_bets, num_simulations, seed)
    return [path[-1] for path in paths]

if __name__ == "__main__":
    result = monte_carlo_simulation(bankroll=1000, strategy=10, odds=-110, win_probability=0.5, num_bets=100, num_simulations=1000, seed=42)
    print(result[:10])
