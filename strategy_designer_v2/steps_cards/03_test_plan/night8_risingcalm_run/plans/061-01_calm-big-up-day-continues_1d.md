---
idea: 061-01_calm-big-up-day-continues
brief: 061_calm-market-big-day-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a coin's one-day rise against the std of its daily returns over the past 30 days, in a calm market -> kept: the 1-day return over the 30-day std, signed; the calm profile is added by code.
- Comparison: the day's move against the coin's 30-day daily-return std -> kept
- Outcome: a larger rise over the next 5 days, in the day's direction, growing with the day's size -> kept: graded position held 5 bars.
- Verdict transfer: yes: the forecast is the idea's measure, and the test asks whether the next 5 days follow it in proportion.
Forecast: One component, `VolatilityScaledReturnComponent` (`period` 1, `vol_period` 30, `lag` 0, `vol_lookback` 1). It gives today's return divided by the std of the last 30 daily returns, today's included. It is standardised over its past 60 values (min 20), so a usual-sized day reads about ±10, capped at ±20. The forecast is positive after an up day and negative after a down day, and it grows linearly with the day's size in swing units. It is 0 only on a flat day. The code keeps the book flat outside the calm profile.
Config: 061-01_calm-big-up-day-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Sample the bars with a nonzero forecast at positions 0, 5, 10, … of each window. Regress each bar's 5-bar forward return, minus that coin's mean 5-bar return over all its windows, on the forecast (`post_pipeline_value`). Pool the coins, sum the deviations of cases on the same day, and read the t of the slope.
- Supporting check: The third of cases with the largest |forecast| has a higher mean directional excess 5-bar return (excess return × sign of forecast) than the third with the smallest |forecast|.
- Confirm: Slope t ≥ 2 with at least 100 cases, and the supporting check passes (largest third above smallest third).
- Reject: Slope t ≤ -2 with at least 100 cases.
- Inconclusive: A slope t between -2 and 2, or t ≥ 2 with the size check failing, or fewer than 100 cases. The minimum is 100 non-overlapping cases inside the calm profile, across all coins.
