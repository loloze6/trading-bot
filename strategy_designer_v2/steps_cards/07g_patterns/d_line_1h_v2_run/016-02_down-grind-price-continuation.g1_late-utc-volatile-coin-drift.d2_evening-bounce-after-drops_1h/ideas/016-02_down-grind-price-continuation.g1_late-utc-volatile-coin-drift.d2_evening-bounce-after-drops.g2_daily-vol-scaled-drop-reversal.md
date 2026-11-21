---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The deeper a coin's 24-hour return falls in units of its 7-day hourly volatility, the larger its rise over the next 24 hours.
Consequence: A trader would buy coins after steep vol-scaled daily drops and hold for a day, a horizon long enough for the move to clear the round-trip cost.
Why:
- F5: Over the next 24 hours, the coin's past 24-hour vol-scaled return predicts a reversal. The OLS slope is -0.0019 (t -4.72, n 15950, non-overlapping daily cases). The lowest vol-scaled-return quintile is followed by roughly +0.004 to +0.007 over 24 hours, the highest by -0.0017 to +0.0002.
- F4: The book loses although the timing is real. Summed gross position gains of 5.34 are outweighed by summed fees of -7.81, and per-trade gross P/L runs from +0.09 % (BTC) to -0.07 % (XRP) against about 0.1 % of commission per trade. The book's daily Sharpe is -0.67 and its mean daily return is -0.00014.
