---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's volatility-scaled 3-day return continues in the same direction over the next 3 days. The larger the past 3-day move relative to its 7-day hourly volatility, the larger the move that follows, most clearly after strong rises.
Consequence: A trader can lean with a coin's strong 3-day move for the following three days rather than fading it.
Why:
- F4: Over three days, moves continue. The next 3-day vol-scaled return regressed on the past 3-day vol-scaled return has slope +0.072 (t 4.15, n 5251), and the slope is positive in all 6 coins (t 0.48 to 2.50). The top fifth of past 3-day moves is followed by +115 bp over the next 3 days (t 4.14, n 1053).
