---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the daily close sits just below past turning-up lows of the last 90 days, the more lows within a few percent above it the stronger -> adapted: the "within a few percent" cut is made graded as the count of clustered swing lows above the close times their nearness.
- Comparison: only while the close is below its 50-day average price -> kept: a regime rule on the close's distance from its 50-day SMA, below 0.
- Outcome: the price falls over the next 5 days, more with more lows -> kept: a short position held 5 bars, sized by the cluster reading.
- Verdict transfer: yes: the test bets short exactly while the close sits under a cluster of past lows below its 50-day average, sized by count and nearness, and is judged on the 5-day fall.
Forecast: The forecast is computed only on bars where the close is below its 50-day SMA. On every other bar it is 0 (flat). The cluster reading looks at the swing lows of the prior 90 daily bars, excluding bar t, with 2 bars on each side. It takes the lowest swing low at or above the close and counts the swing lows within 2 % of that level. It multiplies the count by the nearness 1/(1+D), where D is the percent gap from the close up to the level. The reading is standardised against its own last 90 values, which gives about 10 for a usual reading. Then signed_power with exponent 3 is applied, so a single or distant low gives a forecast near 0 and a tight, near cluster gives a large one. Finally it is negated. The forecast is therefore never positive: it is 0 when no low sits above the close, slightly negative for a single far low, and more negative the more lows are clustered just above the close.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short bets: the forecast falls by at least 2 points on the short side, read once per non-overlapping 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's mean 5-bar return over all its windows, signed for the short side. The measure is the mean of this unusual move over the cases, with its t.
- Supporting check: Split the cases at the median of |forecast|. The mean unusual short-side move of the larger half minus that of the smaller half must be above 0 (more and nearer lows, larger fall).
- Confirm: The mean unusual short-side move is positive with t ≥ 2 over at least 30 cases, and the supporting check is above 0.
- Reject: The mean unusual short-side move is negative with t ≤ -2 over at least 30 cases: price rises more than usual after the signal.
- Inconclusive: Any t between -2 and 2, a confirming t whose supporting check is not above 0, or fewer than 30 independent cases.
