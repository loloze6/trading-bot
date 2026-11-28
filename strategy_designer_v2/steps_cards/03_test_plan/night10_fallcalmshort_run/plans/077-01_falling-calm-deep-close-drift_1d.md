---
idea: 077-01_falling-calm-deep-close-drift
brief: 077_falling-calm-peak-depth-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling calm market, the close's depth below its highest high of the past 20 days, in 20-day daily-return standard deviations -> kept
- Comparison: deeper closes against shallower ones -> adapted: the short position is graded by depth, so deeper closes carry larger shorts
- Outcome: a larger fall over the next three days -> kept
- Verdict transfer: yes: the forecast is the idea's own depth measure inside its own profile, and the test checks whether deeper readings precede larger 3-day falls.
Forecast: The forecast is the close's distance below the highest high of the last 20 days, bar t included. It is computed as (close − H) / H, divided by the standard deviation of the last 20 daily returns. That value is never positive. It is standardised against its own last 60 values, so a usual depth reads about −10, a capped one −20, and a close at the 20-day high reads 0. The forecast is therefore zero at the high and short otherwise. The short grows linearly with the depth in usual daily moves. It is never long. Step 3's code keeps the book flat outside the falling calm profile.
Config: 077-01_falling-calm-deep-close-drift_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The cases are bars with a nonzero forecast, taken on the non-overlapping 3-bar grid of each window. For each case, take the coin's 3-day return minus the coin's mean 3-day return over all its windows (holding the coin). Regress that on the case's forecast (`post_pipeline_value`). The measure is the slope's t, with the cases of one day pooled.
- Supporting check: The book's mean daily return, minus its gain from the market's own fall (position × the coin's mean daily return), must be above 0, before costs.
- Confirm: The slope is positive with t ≥ 2: deeper (more negative) forecasts are followed by lower excess 3-day returns. The supporting check must also pass.
- Reject: The slope is negative with t ≤ −2: deeper closes are followed by relative rebounds.
- Inconclusive: A slope t between −2 and 2. A confirming slope whose supporting check fails is also inconclusive. Any result from fewer than 100 independent cases, or cases on fewer than 60 distinct days, is inconclusive.
