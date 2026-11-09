from src.simulate import monte_carlo_simulation
from src.metrics import avg_result

print("Running Monte Carlo simulation...")
results = monte_carlo_simulation(bankroll=1000, bet=10, odds=-110, win_probability=0.5, num_bets=100, num_simulations=1000, seed=42)
average_result = avg_result(results)
print("Average final bankroll after 1000 simulations:", average_result)