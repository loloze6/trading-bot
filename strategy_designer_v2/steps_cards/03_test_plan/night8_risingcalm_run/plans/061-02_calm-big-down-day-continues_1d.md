---
idea: 061-02_calm-big-down-day-continues
brief: 061_calm-market-big-day-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: one-day fall, large against the 30-day standard deviation of daily returns, in a calm market -> kept: the day's return over its 30-day return std, falls only; the calm profile is added by code.
- Comparison: the fall against the past 30 days' daily-return standard deviation -> kept
- Outcome: the price falls over the next 5 days, more after a larger fall -> kept: a short held 5 bars, sized by the fall.
- Verdict transfer: yes: the forecast is the idea's own graded measure, and each bet is held over its 5-day horizon.
Forecast: Inside the calm profile, the forecast reads `VolatilityScaledReturnComponent` (period 1, vol_period 30). This is today's return divided by the standard deviation of the last 30 daily returns. It is standardised over its past 60 values (min_periods 20), keeping its sign. It is then clipped at a maximum of 0, so only down days count. The forecast is negative (short) on a down day and grows in size with the fall in swing units, capped at -20. It is 0 on up and flat days, and it is never long.
Config: 061-02_calm-big-down-day-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the grid bars t (positions 0, 5, 10, ... of each window) where the forecast is below 0. For each case, compute the position's excess gain: (forecast[t] / 10) x (close[t+5] / close[t] - 1 minus the coin's mean 5-bar return over all its windows). Take the mean of this gain over the cases. Its t counts cases on the same day as one.
- Supporting check: Split the cases at the median of |forecast|. The mean 5-bar excess return, in the short direction, must be larger in the upper half than in the lower half (Welch t ≥ 1).
- Confirm: The mean excess gain is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean excess gain is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 when the supporting check fails, and so is a test with fewer than 100 cases on distinct days.
