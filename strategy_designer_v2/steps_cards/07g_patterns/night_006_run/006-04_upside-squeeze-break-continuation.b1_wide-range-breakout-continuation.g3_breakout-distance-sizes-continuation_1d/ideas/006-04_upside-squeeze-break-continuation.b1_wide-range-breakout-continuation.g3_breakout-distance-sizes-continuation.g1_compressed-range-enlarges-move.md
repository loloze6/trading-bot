---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The narrower a coin's 20-day high-to-low range is relative to its own usual 20-day range width, the larger its absolute price move over the next 10 days, measured in units of its 20-day volatility.
Consequence: A trader would buy volatility, or widen stops and cut size, on a coin whose range has narrowed, rather than treat its low recent volatility as low risk.
Why:
- F1: The 20-day range width sets the size of the next 10 days' move. Measured against the coin's own 20-day volatility (|10-day return| / (20-day daily std × √10)), the move falls steadily across the width quintiles: 1.39, 0.99, 0.80, 0.86 and 0.63, from the narrowest to the widest, with about 165 non-overlapping cases each. So the narrowest ranges are followed by moves more than twice as large, in volatility units, as the widest.
- F2: The narrowest-range quintile is followed by a 10-day absolute move 1.27 times the coin's average, against 0.93 for the other quintiles (Welch t = 3.33, 168 cases vs 659). The ratio is above 1 in every coin, from 1.15 for BTC to 1.41 for XMR. Compression predicts the size of the move but not its direction: the excess 10-day return by width quintile is flat (Spearman ρ = 0.014, p = 0.68).
