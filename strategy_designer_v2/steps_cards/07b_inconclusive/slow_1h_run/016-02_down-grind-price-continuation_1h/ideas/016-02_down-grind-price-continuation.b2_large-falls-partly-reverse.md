---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation
line: 7.b inconclusive
backtest: 016-02_down-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger that 3-day fall, the more the coin rises back over the next 3 days.
Consequence: A trader should not short a large 3-day fall and can lean toward a partial rebound after it.
Why:
- F5: The size of the 3-day fall matters more than how it was built, and it points to reversal. Spearman rho between the past 72-hour return and the excess next-72-hour return is -0.062 (p 0.0015). The largest-fall tercile is followed by +0.0076 and +0.0017 (the low and high forecast halves), while the two smaller-fall terciles are followed by -0.0013 to -0.0097.
- F3: The grind share itself does not grade the outcome, and its strongest grinds lean the wrong way. Recomputed, the five share quintiles from least to most grind give excess 72-hour returns of -0.0023, -0.0060, -0.0022, -0.0031 and +0.0003, with Spearman rho +0.020 (p 0.30).
