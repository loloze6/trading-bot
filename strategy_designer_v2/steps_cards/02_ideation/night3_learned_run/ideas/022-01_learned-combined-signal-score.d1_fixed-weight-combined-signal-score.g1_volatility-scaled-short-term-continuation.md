---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return is next to its 30-day volatility, the higher its return over the next 5 days: a rise that is large for the coin's usual swings keeps rising, and a large fall keeps falling.
Consequence: A trader should follow a coin's recent 3-day move, scaled by its volatility, over the next 5 days rather than fade its last day.
Why:
- F1: The coin's 3-day return divided by its 30-day volatility predicts its next 5-day return in the same direction, the opposite of the reversal this idea assumes. The product with the coin's standardised unusual 5-day move is positive on all five non-overlapping grid offsets, with t of 2.40, 3.22, 5.04, 1.39 and 1.37 on about 2,450 to 2,555 cases each. Lookbacks of 2, 5 and 7 days give similar t values, from 2.2 to 5.0 on offsets 0 to 2.
- F2: The effect is graded. Pooled over all offsets, the unusual 5-day move rises steadily across 3-day z buckets: -1.11 % for z ≤ -2 (261 cases), -0.15 %, -0.32 %, -0.02 %, then +1.29 % for z of 1 to 2 (1,378 cases) and +2.57 % for z > 2 (451 cases).
- F3: The idea's own 1-day reversal leg points the wrong way. Its component product has t -1.21 pooled and -2.04 on XRP. The raw 1-day z-score gives the continuation reading instead: t 2.37 on offset 0 (2,555 cases), and an unusual move of +3.74 % after 1-day z > 2 against -1.52 % after z ≤ -2 (91 and 63 cases).
- F4: The continuation is larger per case than a trade costs. Cases with a 3-day |z| above 1 on the offset-0 grid have an unusual move of +0.90 % and a total move of +0.98 % over 5 days (676 cases), with a strength of 0.080. That is about 4.7 times the 0.19 % round-trip cost.
- F8: By coin, the continuation shows on every offset for XRP (t 1.30 to 2.67), BTC (0.93 to 2.13) and ETH (0.83 to 2.74). It is weak or mixed for LTC (-0.53 to 1.40), XMR (-0.76 to 1.02) and ZEC (-0.67 to 2.35).
