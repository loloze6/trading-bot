---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the 24 hours up to the 20:00 UTC close, measured in units of its own past-30-day hourly volatility, the more it rises over the next 24 hours.
Consequence: Rank evening falls by their size against the coin's normal volatility, so that small, ordinary dips no longer draw a position that pays fees for nothing.
Why:
- F2: Across 6,958 trades the mean is -0.60% before fees and -0.70% after them, with 0.43% of commission per trade and 49% winners. The trades that carry no edge are paying fees.
- F3: The gain sits only in the extreme falls. Over the 8,538 long 20:00 bars, the two weakest forecast quintiles (forecast about 1.4 and 4.6) earn about -0.0011 of next-24h excess return each. Measured in the coin's own 30-day hourly volatility, only the deepest fifth of falls (z about 1.69) earns a positive 0.0054, while the other four fifths average about -0.0009.
