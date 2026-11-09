# Monte-Carlo-Simulator

Simulates sports betting bankrolls with Monte Carlo methods to see how odds, win probability, and bet sizing affect long-run results.

## Setup

```
pip install -r requirements.txt
```

## Usage

Run commands from the project root.

```
python -m experiments.run_baseline   # run the baseline simulation
python -m pytest                     # run the tests
```

## Project layout

- `src/odds.py` – converts moneyline odds to a return multiplier
- `src/simulate.py` – single bet, bet sequence, and Monte Carlo simulation
- `src/metrics.py` – summary statistics for simulation results
- `src/strategies.py` – bet sizing strategies
- `experiments/` – scripts that run simulations
- `tests/` – unit tests
