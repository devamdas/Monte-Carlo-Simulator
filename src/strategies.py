from src.odds import odds_to_return

"Each strategy decides how much to bet given the current bankroll"
"bet_size(bankroll) -> amount to bet (0 means skip this bet)"
"record(won) -> lets strategies that depend on past results update themselves"
"reset() -> clears any memory before a new simulation starts"


class FlatBet:
    "Bets the same amount every time"
    def __init__(self, amount: float):
        self.amount = amount

    def bet_size(self, bankroll: float) -> float:
        return self.amount

    def record(self, won: bool):
        pass

    def reset(self):
        pass


class PercentBet:
    "Bets a fixed fraction of the current bankroll"
    def __init__(self, fraction: float, min_bet: float = 1):
        self.fraction = fraction
        self.min_bet = min_bet

    def bet_size(self, bankroll: float) -> float:
        return max(bankroll * self.fraction, self.min_bet)

    def record(self, won: bool):
        pass

    def reset(self):
        pass


def kelly_fraction(win_probability: float, odds: float) -> float:
    "Kelly formula f = (b*p - q) / b, where b is profit per $1 bet; 0 if there's no edge"
    b = odds_to_return(odds) - 1
    q = 1 - win_probability
    return max((b * win_probability - q) / b, 0)


class KellyBet(PercentBet):
    "Bets the Kelly fraction of the bankroll; multiplier=0.5 gives half Kelly"
    def __init__(self, win_probability: float, odds: float, multiplier: float = 1.0, min_bet: float = 1):
        super().__init__(kelly_fraction(win_probability, odds) * multiplier, min_bet)

    def bet_size(self, bankroll: float) -> float:
        if self.fraction == 0:
            return 0
        return super().bet_size(bankroll)


class Martingale:
    "Doubles the bet after each loss and goes back to the base bet after a win"
    def __init__(self, base_bet: float):
        self.base_bet = base_bet
        self.current_bet = base_bet

    def bet_size(self, bankroll: float) -> float:
        return min(self.current_bet, bankroll)

    def record(self, won: bool):
        self.current_bet = self.base_bet if won else self.current_bet * 2

    def reset(self):
        self.current_bet = self.base_bet
