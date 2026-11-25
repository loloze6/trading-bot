---
idea: 058-01_agitated-decline-rally-giveback
brief: 058_falling-agitated-multiday-rallies-fail
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: a coin's 3-day rise in a falling, agitated market -> kept: the profile is added by code, and the forecast is graded by the rise; it is zero when there is no rise.
- Comparison: the rise measured against the standard deviation of daily returns over the past 30 days -> kept
- Outcome: a larger fall over the next 5 days, taking back a larger share of the rise -> kept: short 5 bars, graded by the scaled rise; the share is tested in the check.
- Verdict transfer: yes: the forecast is the idea's own scaled 3-day rise, inside its own profile, held short for its own 5-day horizon.
Forecast: The forecast uses one indicator, the 3-day return divided by the 30-day standard deviation of daily returns (times sqrt(3), a constant). It is standardised over its past 60 values. It is then clipped at 0, so only rises count, and negated. The forecast is therefore zero when the coin has not risen over 3 days. It is negative after a rise, and its size grows linearly with the rise in usual moves, capped at -20. It is never positive. Code adds the falling-agitated profile, so the book is flat outside that profile.
Config: 058-01_agitated-decline-rally-giveback_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case, in the short direction. A case is a short bet (the forecast falls by at least 2 points), read once per 5-bar grid cell. The move is the coin's 5-day return from that bar minus the coin's normal 5-day drift. Report its mean and t, with the cases of one day pooled.
- Supporting check: The share given back per case, defined as -(the unusual 5-day move) divided by the 3-day rise. Compare cases in the top half of |forecast| against the bottom half: Welch t of top minus bottom.
- Confirm: The mean unusual move in the short direction is above 0 with t >= 2, and the supporting check gives a Welch t >= 2.
- Reject: The mean unusual move in the short direction has t <= -2, meaning rises continue, or the share-given-back difference has a Welch t <= -2.
- Inconclusive: Any other result, including t between -2 and 2 on either measure, is inconclusive. So is a test with fewer than 30 cases or fewer than 30 distinct days.
