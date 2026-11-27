---
idea: 077-01_falling-calm-deep-close-drift
brief: 077_falling-calm-peak-depth-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: the close sits below its highest high of the past 20 days, measured in 20-day daily-return standard deviations, in a falling, calm market -> kept (the profile is added by code; the depth is graded on every profile bar)
- Comparison: deeper closes against shallower ones -> kept (the position grows with the depth, zero at the high)
- Outcome: a larger fall over the next three days -> kept (short, held 3 bars)
- Verdict transfer: yes: the forecast is the idea's own depth measure, short and graded inside its profile, judged over its own 3-day horizon.
Forecast: Use VolatilityScaledDistanceFromHighComponent with period 20, vol_period 20, source "high", exclude_current 0 and base "level". It computes (close − highest high of the last 20 bars, today included) / that high / the std of the last 20 daily returns. That value is 0 at the high and never positive. It is standardised over its past 60 values (min_periods 20) and not negated. The forecast is therefore 0 when the close is at the 20-day high and grows more negative (a larger short) the more usual daily moves the close sits below it. Its average size is about −10, capped at −20. It is never long. Outside the falling, calm profile the book is flat (added by code).
Config: 077-01_falling-calm-deep-close-drift_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Cases are bars with a non-zero forecast on a non-overlapping 3-bar grid per window. For each case, take the coin's 3-bar forward return minus the coin's mean 3-bar return over all its windows (holding the coin). Measure the slope of that excess return on the forecast, before costs. A positive slope means deeper (more negative) forecasts are followed by larger excess falls.
- Supporting check: The mean excess 3-bar return of the deepest third of cases (most negative forecasts) minus that of the shallowest third is below 0.
- Confirm: The slope is positive with t ≥ 2 and the supporting check passes (deepest third minus shallowest third < 0).
- Reject: The slope is negative with t ≤ −2: deeper closes are followed by smaller falls or rebounds.
- Inconclusive: A slope with |t| < 2, or a positive slope with t ≥ 2 while the deepest-minus-shallowest difference is not below 0. Fewer than 50 independent cases is also inconclusive.
