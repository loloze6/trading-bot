---
idea: 050-02_falling-calm-scaled-week-rise-continuation
brief: 050_calm-downtrend-scaled-weeks-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: a coin that has risen over the last 7 days, in a falling calm market -> kept: the 7-day return clipped at 0, so nothing is held after a 7-day fall; the profile is added by code.
- Comparison: the 7-day rise in units of the coin's 30-day daily-return swing -> kept: the 7-day return over the 30-day std of daily returns (the constant sqrt(7) cancels under standardise).
- Outcome: the coin keeps rising over the next 3 days, further for larger scaled rises -> kept: long, graded by the scaled rise, held 3 bars.
- Verdict transfer: yes: the forecast is exactly the idea's scaled 7-day rise inside its profile, held for its 3-day horizon.
Forecast: One component, VolatilityScaledReturnComponent with period 7 and vol_period 30. It is the 7-day return divided by (the std of the last 30 daily returns x sqrt 7). It is standardised over its past 60 values (min 20), so a usual-sized reading gives about 10, capped at 20. It is then clipped at 0. The forecast is positive and grows with the 7-day rise in usual moves. It is exactly 0 when the coin did not rise over the last 7 days. It is never short. The code keeps the book flat outside the falling calm profile.
Config: 050-02_falling-calm-scaled-week-rise-continuation_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move of the cases over 3 bars. A case is a forecast rise of at least 2 points, read once per non-overlapping 3-bar grid cell. The unusual move is the 3-bar return from the signal bar's close minus the coin's normal 3-bar drift over all its windows, taken long. Its t is computed with the cases of one day taken together.
- Supporting check: Size dependence. Among the cases, the mean unusual move of those with a forecast at or above the cases' median, minus that of those below it (Welch t), is above 0.
- Confirm: The unusual move has t ≥ 2 and the supporting check's difference is positive.
- Reject: The unusual move has t ≤ -2, meaning the scaled rises are followed by a reliable fall against the coin's drift.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 with a non-positive size difference is also inconclusive. So is a test with fewer than 30 cases or fewer than 30 distinct days.
