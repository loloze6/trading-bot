---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the coin's 30-day return is positive, and its daily volume is high relative to its own 20-day average -> kept: a 30-bar return above 0 is a regime rule, and the volume ratio over 20 bars sets the size.
- Comparison: higher volume ratio against lower volume ratio, among rising coins -> kept: the long position grows continuously with the volume ratio.
- Outcome: a higher return over the next 3 days, on the long side -> kept: the 3-day horizon is 3 bars, and the return is measured against the coin's average.
- Verdict transfer: yes: a positive slope of the 3-day return on the volume ratio, in rising coins only, is the idea itself, and a negative slope contradicts it.
Forecast: The forecast is active only on bars where the 30-bar price change is above 0; on every other bar it is 0 (flat). On active bars it is the 20-bar volume ratio, put on the forecast scale by standardise (about 10 at the usual volume level). A signed_power with exponent 2 and pivot 10 then acts as a graded dead zone. On thin volume the long position shrinks smoothly towards 0, which refuses the trade. On heavy volume the position is amplified, up to the +20 cap. The forecast is never negative.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The sample is the trending-regime bars that fall on each window's grid of non-overlapping bars (positions 0, 3, 6, ...). On these bars, regress the coin's 3-bar forward return, minus that coin's mean 3-bar return over all its windows, on the recorded `volratio` last_history_value. The measure is the OLS t-statistic of the slope.
- Supporting check: none
- Confirm: The slope is positive with t >= 2, from at least 100 independent grid cases.
- Reject: The slope is negative with t <= -2, from at least 100 independent grid cases.
- Inconclusive: Any t between -2 and +2 is inconclusive, as is fewer than 100 trending-regime grid cases across all coins and windows.
