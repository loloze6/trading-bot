---
idea: 027-01_panic-range-multiple-rebound
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 3503e22a3698
---
Fidelity:
- Situation: a 24-hour fall whose high-low range is a large multiple of the 30-day average 24-hour range -> adapted: the on/off "falls" condition is made graded. The reading is the 24h fall's depth in usual 24h moves times the 24h range in multiples of its 30-day mean (6 and 180 bars). It is 0 when there is no fall.
- Comparison: more than the coin's usual return -> kept: the excess over the coin's mean 84-bar return across all windows.
- Outcome: higher return over the next 14 days, growing with the range multiple -> kept: an 84-bar hold, with the position growing with the multiple.
- Verdict transfer: yes: the forecast rises with a falling 24h stretch's range multiple, and each bet is held 14 days and judged against the coin's drift.
Forecast: The forecast uses ScaledFallRangeMultipleComponent (period 6, lag 0, window 180) on 4h bars. Its reading is the last 24h fall in usual 24h moves times the last 24h high-low range in multiples of its 30-day mean. It is exactly 0 when the last 24h did not fall. The reading is standardised against its own past 192 values (min 48). It then passes through signed_power with exponent 3, the strongest graded dead zone. Ordinary falls stay near 0, and only large panic multiples give a sizeable long. The forecast is never negative (long only), it grows with the fall and the range multiple, and it is 0 when there is no fall.
Config: 027-01_panic-range-multiple-rebound_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: The mean unusual move over all coins and windows. A case is a long bet: a forecast rise of at least 2 points, read once per non-overlapping 84-bar grid cell. Its unusual move is the coin's 84-bar return from the case's close minus that coin's normal 84-bar drift (its mean over all windows). The measure is this mean with its t, before costs.
- Supporting check: The gradient across cases. Split the cases at the median forecast at entry; the mean unusual move of the upper half minus the lower half (Welch t) must be above 0.
- Confirm: The mean unusual move is positive with t ≥ 2, and the upper-minus-lower difference is above 0.
- Reject: The mean unusual move is negative with t ≤ -2.
- Inconclusive: Any other result, including t between -2 and 2, or t ≥ 2 with a gradient at or below 0. With fewer than 30 cases over all coins and windows, the result is also inconclusive.
