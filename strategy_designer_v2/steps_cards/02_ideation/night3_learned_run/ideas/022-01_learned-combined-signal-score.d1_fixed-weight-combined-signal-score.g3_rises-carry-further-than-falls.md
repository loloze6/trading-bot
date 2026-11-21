---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day rise is next to its 30-day volatility, the more its return over the next 5 days exceeds its normal drift, by more than the same-sized fall predicts on the downside.
Consequence: A trader should weight the long side of short-term continuation more than the short side.
Why:
- F2: The effect is graded. Pooled over all offsets, the unusual 5-day move rises steadily across 3-day z buckets: -1.11 % for z ≤ -2 (261 cases), -0.15 %, -0.32 %, -0.02 %, then +1.29 % for z of 1 to 2 (1,378 cases) and +2.57 % for z > 2 (451 cases).
- F4: The continuation is larger per case than a trade costs. Cases with a 3-day |z| above 1 on the offset-0 grid have an unusual move of +0.90 % and a total move of +0.98 % over 5 days (676 cases), with a strength of 0.080. That is about 4.7 times the 0.19 % round-trip cost.
- F6: The continuation is stronger after rises than after falls. Its strength is 0.107 after a 3-day z above 1 (381 cases, unusual move +1.33 %) and 0.045 after a z below -1, read in the signal's direction (295 cases, +0.35 %).
