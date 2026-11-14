---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its long moving average but has pulled back into the lower part of its recent range, with a recent change that is falling, its return over the following days is below its usual drift. The deeper the pullback, the weaker that return.
Consequence: Refuse to buy dips inside an uptrend, and step aside until price recovers toward its recent high.
Why:
- F3: Being above the long average adds nothing by itself: next-day coin return is 0.001187 in the trending regime and 0.001193 in the unknown regime. The same momentum-near-high ranking separates returns only when the coin is trending (high minus low t 2.77 at 1 bar, 3.05 at 5 bars) and not when it is below the average (t 0.15 at 1 bar, −0.47 at 5 bars).
- F5: Within the trending regime, pullbacks are followed by below-average returns. Trending bars with a zero forecast have a mean 1-bar excess of −0.0024 (2440 cases) and a 5-bar excess of −0.0118 (474), and the weakest 20-day-rise quintile has a next-day mean of −0.0018.
