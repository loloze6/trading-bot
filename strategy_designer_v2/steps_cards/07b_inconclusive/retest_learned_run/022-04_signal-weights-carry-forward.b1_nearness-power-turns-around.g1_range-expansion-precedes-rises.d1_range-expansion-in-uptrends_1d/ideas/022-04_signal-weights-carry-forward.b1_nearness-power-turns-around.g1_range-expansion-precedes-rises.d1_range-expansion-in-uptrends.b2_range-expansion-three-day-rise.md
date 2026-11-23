---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's daily high-low range is relative to its average range over the past 30 days, the higher that coin's return over the next 3 days, only while the coin's own 20-day return is positive.
Consequence: A trader in a coin that is rising over 20 days could add to a long position after an unusually wide day and expect the gain within about three days.
Why:
- F3: The raw range ratio (today's range over its 30-day mean) predicts more clearly than the standardised forecast. In trending bars its 5-day slope has t 2.12 (1,281 cases) on offset 0, and t 5.51, 3.59, 1.15 and 2.56 on the other offsets. At 3 days it has t 5.21 (2,167 cases) and at 10 days t 4.73 (623 cases).
- F4: The uptrend condition carries the effect. While the 20-day return is at or below zero, the ratio's slope is −0.0035 (t −0.69, 1,274 cases) at 5 days and −0.0078 (t −0.88) at 10 days. In a pooled 5-day regression, the ratio-times-uptrend term is +0.013 (t 1.92), while the ratio alone is −0.0035 (t −0.67).
- F5: The effect is uneven across coins and years.
