---
idea: 047-01_falling-agitated-scaled-fall-rebound
brief: 047_agitated-downtrend-scaled-days-reverse
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a down day in a falling, agitated market -> kept: the profile is added by code, and the forecast is 0 on every bar that did not close down.
- Comparison: the day's fall in units of its 30-day daily-return swing -> kept: the one-day return divided by the 30-day standard deviation of daily returns.
- Outcome: a rise over the next 3 days, larger the larger the scaled fall -> kept: long for 3 bars, sized by the scaled fall.
- Verdict transfer: yes: the forecast is the scaled fall on down days inside the profile, held for the idea's 3 days.
Forecast: The forecast uses one component, `VolatilityScaledReturnComponent` with `period` 1, `vol_period` 30 and `lag` 0. It gives the day's return divided by the standard deviation of the last 30 daily returns. The value is standardised over its past 60 values (`min_periods` 20), then negated, then clipped at 0. The forecast is therefore exactly 0 on up and flat days. On a down day it is positive and grows linearly with the fall in usual daily moves, capped at 20. It is never negative. The code adds the falling-agitated profile, so the book is flat outside it.
Config: 047-01_falling-agitated-scaled-fall-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: A case is a bar of each window's non-overlapping 3-bar grid where the forecast is above 0. For each case, take the coin's 3-day return from that close minus the coin's normal 3-day drift (its mean over all windows). The measure is the mean of these unusual moves and its t, with same-day cases summed per day.
- Supporting check: Compute the slope of the per-case unusual move on the case's forecast (least squares, cases as above). It passes if the slope is above 0.
- Confirm: Both of these hold: - the mean unusual move is positive with t >= 2 over at least 30 case-days; - the slope on the forecast is positive.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 case-days.
- Inconclusive: Any of these is inconclusive: - t between -2 and 2; - t >= 2 with a slope at or below 0; - fewer than 30 case-days.
