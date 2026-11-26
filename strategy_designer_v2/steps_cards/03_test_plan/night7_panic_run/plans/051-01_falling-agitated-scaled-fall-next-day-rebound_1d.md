---
idea: 051-01_falling-agitated-scaled-fall-next-day-rebound
brief: 051_agitated-downtrend-falls-rebound-next-day
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f9d41455da54
---
Fidelity:
- Situation: a down day in a falling, agitated market -> kept: the profile is added by code, and the clipped scaled fall is exactly 0 on up and flat days.
- Comparison: the day's fall in units of the coin's 30-day standard deviation of daily returns -> kept: the one-day return divided by the 30-day return standard deviation.
- Outcome: the coin rises over the next day, more after a larger scaled fall -> kept: a long position graded by the scaled fall, held 1 bar.
- Verdict transfer: yes: the forecast is the idea's own scaled fall inside its profile, judged on the next day's move.
Forecast: One component, `VolatilityScaledReturnComponent` with `period` 1 and `vol_period` 30. Its raw value is today's return divided by the standard deviation of the last 30 daily returns. `standardise` (window 60, min_periods 20) scales it against its own past values. `negate` turns falls positive, and `clip` at min 0 removes up days. The forecast is 0 on up and flat days. On a down day it is positive and grows linearly with the size of the fall in usual daily moves, capped at 20. It is never negative (long only). Code keeps the book flat outside the falling agitated profile.
Config: 051-01_falling-agitated-scaled-fall-next-day-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Over the cases (bars with forecast above 0), the unusual move: close[t+1]/close[t] − 1 minus the coin's mean daily return over all its windows. Its t is computed with the cases of one day pooled.
- Supporting check: Over the same cases, the slope of the next-day unusual move on the forecast is positive, with t ≥ 2 (cases of one day pooled).
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting slope is positive with t ≥ 2.
- Reject: The mean unusual move is below 0 with t ≤ −2, or the slope is negative with t ≤ −2.
- Inconclusive: Any other result, including a positive unusual move whose slope is not significant. Fewer than 30 distinct case days is also inconclusive.
