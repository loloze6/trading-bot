---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days.
Consequence: A trader would follow a coin's 30-day trend over the next 5 days, not fade it.
Why:
- F2: The theory's own test fails. Reversion toward the middle of the 30-day range is nil in flat coins (mean signed excess move 0.011 usual moves, t 0.39, 917 cases). In trending coins (ratio above 0.33) the move goes the other way, away from the middle (−0.072, t −2.93, 1638 cases): a trend that continues, not a reversion.
- F8: In trending coins, the 30-day move continues over the next 5 days, more strongly the larger it is, except for the very largest moves:
