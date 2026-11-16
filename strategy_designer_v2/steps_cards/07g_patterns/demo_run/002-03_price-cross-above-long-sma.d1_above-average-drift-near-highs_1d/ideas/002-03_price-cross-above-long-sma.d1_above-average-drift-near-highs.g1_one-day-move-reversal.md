---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its usual daily move, the larger its rise over the next day; a large one-day rise is followed by a smaller, opposite fall the next day.
Consequence: A trader would avoid adding to a trend-following long on the day after a sharp rise, and would let a sharp one-day fall in an uptrend be bought rather than sold.
Why:
- F1: A coin's next-day return reverses its previous day's move, and the reversal grows with the size of that move. These are next-day returns minus the coin's mean, grouped by the previous day's return standardised per coin:
- F5: The book's gain comes from long holds:
