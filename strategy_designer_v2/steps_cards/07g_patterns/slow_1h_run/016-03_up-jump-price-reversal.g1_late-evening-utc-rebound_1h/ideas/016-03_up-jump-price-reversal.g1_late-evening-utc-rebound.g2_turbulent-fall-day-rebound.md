---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high relative to its 7-day volatility, the more it has fallen over its last 24 hours, the more it rises over the next 24 hours.
Consequence: Lean harder into buying 24-hour falls when the coin's recent hours have been unusually turbulent, and less in calm stretches.
Why:
- F4: The 24-hour reversal is strongest when recent volatility is high against the week's. In the top fifth of 24-hour versus 168-hour volatility, the slope is −0.107 (t −8.47, n 3,249) against −0.065 (t −2.41) in the bottom fifth, and that top fifth also gains +34.4 bps over the next 24 hours on average (t 3.40).
- F3: The 24-hour reversal behind the idea holds over a full day, not only 2 hours. On a non-overlapping 24-bar grid, the slope of the next 24-hour return on the past 24-hour return is negative in every coin (−0.064 to −0.129, t −3.4 to −6.9, about 2,800 cases each) and in seven of eight years. The deepest-fall fifth gains +58.5 bps over the next 24 hours (t 5.69, n 3,423), while the 72-hour version is not significant (slope +0.016, t 1.16, n 5,539).
