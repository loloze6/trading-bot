---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a high extreme on BTC, ETH or BNB -> adapted: the threshold is made graded (RSI above 50, sharply amplified toward extremes), and "after" is made "while".
- Comparison: more than after neutral readings -> kept: neutral RSI gives a forecast near zero, so forward returns can be compared across forecast sizes.
- Outcome: price keeps rising over the following bars -> kept: measured as the forward return on long positions.
- Verdict transfer: yes: a long position sized by how extreme a high RSI reading is earns above holding only if high extremes precede further rises, and earns below holding only if they do not.
Forecast: The forecast uses the 14-bar Wilder RSI on daily closes. The component outputs 50 − RSI, which is standardised against its own last 60 values (average absolute value about 10) and then negated, so it reads RSI − 50. A clip at 0 removes the readings below 50, because the idea concerns only high extremes; a low RSI gives zero. A signed power with exponent 3 and pivot 10 is then applied. This makes the forecast near zero for neutral or mildly high RSI (5 becomes 1.25). It reaches 10 when RSI is high relative to its usual range and the 20 cap at strong extremes. The forecast is never negative, and it grows smoothly with how far RSI sits above 50.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after bars with forecast ≥ 10, minus the coin's mean 5-bar return over all bars of all 24 windows together (holding). It is pooled over the three coins, uses non-overlapping 5-bar blocks so that overlapping returns count once, is judged before costs, and is reported as a t-statistic.
- Supporting check: The mean 5-bar forward return after bars with forecast ≥ 10, minus the mean after neutral bars (forecast < 1), with a t-statistic on non-overlapping blocks.
- Confirm: The main-measure excess is positive with t ≥ 2, and the supporting difference over neutral bars is positive.
- Reject: The main-measure excess is negative with t ≤ -2, meaning prices fall relative to holding after high extremes.
- Inconclusive: Any t between -2 and 2, including estimates near zero or merely on the wrong side of zero. It is also inconclusive if there are fewer than 30 non-overlapping 5-bar cases with forecast ≥ 10, pooled across the three coins.
