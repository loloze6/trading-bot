---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: latest one-day return relative to 30-day daily volatility, while the 30-day return is positive -> kept: 1-bar return over 30-bar return std, in a regime gated on the 30-bar return above 0.
- Comparison: larger versus smaller volatility-scaled day within up-months -> kept: the position grows with the volatility-scaled return.
- Outcome: higher return over the next 7 days -> kept: the 7-bar forward return, judged against the coin's average.
- Verdict transfer: yes: the forecast is the idea's own measure under its own condition, and the 7-bar outcome is measured directly.
Forecast: The regime is "trending" when the 30-bar percent return (PriceEvolutionComponent, period 30) is above 0. On all other bars the regime is flat. In "trending", the forecast is the latest 1-bar return divided by the standard deviation of the last 30 one-bar returns (VolatilityScaledReturnComponent, period 1, vol_period 30). It is standardised over its past 60 values (min_periods 20). It is positive after an up day and negative after a down day, and it grows with the day's size in usual moves, capped at ±20.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Take the non-overlapping 7-bar grid of each window, using only grid bars whose regime is "trending". Compute each bar's 7-bar forward return minus that coin's mean 7-bar return over all windows. Measure the OLS slope of this excess return on the bar's forecast, and its t-statistic.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2, on at least 100 independent grid cases pooled across coins and windows.
- Reject: The slope is negative with t ≤ -2, on at least 100 independent cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. Fewer than 100 trending grid cases is also inconclusive, whatever the t.
