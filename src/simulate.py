import random
from src.odds import odds_to_return

def simulate_bet(bankroll: float, bet: float, odds: float, win_probability: float, rng=random) -> float:
    if rng.random() < win_probability:
        profit = bet * (odds_to_return(odds) - 1)
        return bankroll + profit
    else:
        return bankroll - bet
def simulate_seq(bankroll: float, bet: float, odds: float, win_probability: float, num_bets: int, rng=random) -> float:
    for _ in range(num_bets):
        bankroll = simulate_bet(bankroll, bet, odds, win_probability, rng)
    return bankroll
def monte_carlo_simulation(bankroll: float, bet: float, odds: float, win_probability: float, num_bets: int, num_simulations: int, seed=None) -> list:
    rng = random.Random(seed)
    results = []
    for _ in range(num_simulations):
        final_bankroll = simulate_seq(bankroll, bet, odds, win_probability, num_bets, rng)
        results.append(final_bankroll)
    return results

if __name__ == "__main__":
    result = monte_carlo_simulation(bankroll=1000, bet=10, odds=-110, win_probability=0.5, num_bets=100, num_simulations=1000, seed=42)
    print(result[:10])
