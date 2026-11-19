---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen sharply over the past day relative to its usual hourly volatility, it rises over the next day. The deeper the volatility-scaled 1-day fall, the larger the next-day rebound.
Consequence: A trader can buy a coin after an unusually deep one-day drop, expecting part of it back within a day, and should refuse to short into such a drop.
Why:
- F3: A large one-day fall is followed by a rebound over the next day. On non-overlapping 24-hour samples, the lowest fifth of past-day return scaled by 7-day hourly volatility is followed by a mean +55 bp next day (t 5.56, n 3251). The other four fifths range from −6.7 to +5.5 bp, all with |t| < 0.8. On raw past-day return the lowest fifth gives +59 bp (t 5.54).
