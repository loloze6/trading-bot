---
idea: 077-01_choppy-calm-swing-rise-carries
brief: 077_choppy-calm-swing-scaled-moves-carry
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ad4516fba127
---
Fidelity:
- Situation: in a choppy, calm market, the 14-day return is large and positive against the coin's daily swing over the past 30 days -> kept: the profile is added by code, and "large and positive" is a regime: the 14-day return is at least one usual 14-day move (the daily std times √14, the conventional line between ordinary and large); inside it the size is graded.
- Comparison: the coin's own daily swing over the past 30 days -> kept: the 14-day return is divided by the std of the last 30 daily returns (times √14, a constant factor).
- Outcome: keeps rising over the next 7 days, more after a larger swing-scaled rise -> kept: long for 7 bars, sized by the swing-scaled rise.
- Verdict transfer: yes: the test measures the idea's own rise, swing scale, profile, side and horizon.
Forecast: The forecast is the 14-day return divided by (the std of the last 30 daily returns × √14), from VolatilityScaledReturnComponent with period 14 and vol_period 30. It is standardised against its own last 60 values (min_periods 20) and clipped at 0. It is non-zero only in the regime where that same reading is at least 1.0, one usual 14-day move, and only inside the choppy calm profile. There it is long, about +10 to +12 at the threshold, and it grows with the swing-scaled rise up to the cap of 20. Everywhere else it is 0 (flat). It is never short.
Config: 077-01_choppy-calm-swing-rise-carries_1d_config.json
Profile: choppy calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: the mean unusual move over the cases (forecast rises of at least 2 points, one per 7-bar grid cell). It is the coin's 7-bar return after the signal bar minus its mean 7-bar return over all windows, with its t computed on cases grouped by day.
- Supporting check: across the cases, the mean unusual move of the cases above the median forecast minus that of the cases below it is greater than 0.
- Confirm: the mean unusual move is above 0 with t ≥ 2, and the supporting check passes.
- Reject: the mean unusual move is below 0 with t ≤ -2.
- Inconclusive: any t between -2 and 2, or t ≥ 2 with the supporting check failing. At least 30 case-days are needed, otherwise the result is inconclusive.
