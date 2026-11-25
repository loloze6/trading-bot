---
idea: 059-01_choppy-calm-weekly-rise-continues
brief: 059_choppy-calm-weekly-rise-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: a coin's rise over the past 7 days, set against its usual daily swing over the past 30 days, in a choppy calm market -> adapted: graded as the 7-bar return over the 30-bar standard deviation of daily returns, long only when that return is positive; the choppy calm profile is added by code.
- Comparison: the rise's size against the usual daily swing -> kept
- Outcome: a further rise over the next 7 days that grows with the scaled rise -> kept
- Verdict transfer: yes: the forecast is the idea's scaled weekly rise inside its profile, held for its 7-day horizon.
Forecast: The indicator is VolatilityScaledReturnComponent with `period` 7, `vol_period` 30 and `lag` 0. It gives the 7-day return divided by (the 30-day standard deviation of daily returns x sqrt 7). The sqrt 7 is a constant, and `standardise` (window 60, min_periods 20) cancels it. After `standardise`, a `clip` with `min` 0 keeps only rises. The forecast is 0 when the past week fell or was flat. It is positive after a rise and grows linearly with the rise's size in usual daily swings, about +10 for a typical-sized move and capped at +20. It is never negative. Outside the choppy calm profile, code keeps it at 0.
Config: 059-01_choppy-calm-weekly-rise-continues_1d_config.json
Profile: choppy calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: The cases are bars on each window's non-overlapping 7-bar grid with forecast > 0. For each case, take the coin's 7-bar forward return minus its normal 7-bar drift (the mean over all windows). Regress that excess return on the forecast; the measure is the slope's t.
- Supporting check: The mean excess 7-bar return of the same cases (the unusual move), with its t computed with cases on the same day taken together, must be above 0.
- Confirm: The slope's t is 2 or more, and the mean excess return is above 0, with at least 40 cases.
- Reject: Either the slope's t is -2 or less, or the mean excess return's t is -2 or less (a giveback), with at least 40 cases.
- Inconclusive: Any other result, or fewer than 40 cases with forecast > 0 on the grid.
