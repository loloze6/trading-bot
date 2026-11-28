---
idea: 090-01_calm-decline-scaled-push-continues
brief: 090_falling-calm-scaled-push-carries
data-instruments: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 5a7846f8b001
---
Fidelity:
- Situation: the coin's 5-day return divided by the standard deviation of its daily returns over 30 days, in a falling calm market -> kept: `VolatilityScaledReturnComponent` (period 5, vol_period 30). Its extra constant factor sqrt(5) cancels under standardise. The profile is added by code.
- Comparison: the larger the scaled push upward, the larger the rise, and the weaker or more negative, the smaller -> kept: the forecast and the measure are graded in the scaled push.
- Outcome: the coin rises over the next 5 days -> kept: 5-day forward return, net of the coin's drift.
- Verdict transfer: yes: the scaled push is measured exactly, inside the profile, over the idea's own 5-day horizon.
Forecast: The forecast is the coin's 5-day return over its 30-day daily-return standard deviation, from `VolatilityScaledReturnComponent` with period 5 and vol_period 30. It is standardised against its last 60 values (min_periods 20), so a typical push gives about 10, capped at 20. It is then clipped at 0, because the brief is long only. The forecast is positive and grows with the size of an upward push. It is 0 when the 5-day return is zero or negative. Outside the falling calm profile it is 0 (added by code).
Config: 090-01_calm-decline-scaled-push-continues_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-day forward return, minus its mean 5-day return over all windows, on the recorded raw push `push.last_history_value`. - Samples: in-profile bars on the non-overlapping 5-bar grid of each window. - Pooling: over all coins, with cases on the same day taken together. - Statistic: the t of the slope.
- Supporting check: The mean unusual 5-day move of the cases (forecast rises of at least 2 points) is above 0.
- Confirm: The slope's t is 2 or more, the check passes, and there are at least 100 samples.
- Reject: The slope's t is -2 or less, with at least 100 samples.
- Inconclusive: The slope's t is between -2 and 2. A t of 2 or more with the check failing is also inconclusive. So is any result from fewer than 100 non-overlapping in-profile samples or fewer than 30 cases.
