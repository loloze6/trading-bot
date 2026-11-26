---
idea: 058-01_choppy-agitated-weekly-rise-continues
brief: 058_choppy-agitated-weekly-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a choppy, agitated market, the coin's 7-day return is a rise -> adapted: the profile is added by code, and the rise is kept as a long-only graded forecast that is 0 when the 7-day return is not a rise.
- Comparison: the 7-day rise against the coin's usual daily swing over the past 30 days -> kept: the 7-day return divided by the 30-day standard deviation of daily returns.
- Outcome: the price rises further over the next 7 days, more after larger scaled rises -> kept: a 7-bar holding period, judged by the excess 7-day return and its relation to the forecast size.
- Verdict transfer: yes: the forecast is the idea's scaled 7-day rise, held only inside the profile for the idea's 7-day horizon.
Forecast: The forecast uses `VolatilityScaledReturnComponent` with `period` 7, `vol_period` 30, `lag` 0 and `vol_lookback` 1. - Raw value: the 7-day return divided by the 30-day standard deviation of daily returns times sqrt(7). The sqrt(7) is a constant and cancels under `standardise`. - Scale: `standardise` (window 60, min_periods 20) puts it on the forecast scale, about 10 for a typical size. - Long only: a `clip` at min 0 removes the short side. - Sign and size: the forecast is positive and grows linearly with the 7-day rise measured in usual daily swings. It is exactly 0 when the 7-day return is flat or a fall, so no position exists outside the idea's situation. - Profile: code adds the choppy agitated profile, which keeps the book flat outside it.
Config: 058-01_choppy-agitated-weekly-rise-continues_1d_config.json
Profile: choppy agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: On a non-overlapping 7-bar grid per window, take the cases where the forecast is above 0. For each case, compute the coin's 7-bar forward return minus its mean 7-bar return over all windows (holding the coin). Report the mean of this excess return, with its t (cases of one day taken together).
- Supporting check: Across the same cases, the Spearman correlation between the forecast and the excess 7-bar return is above 0.
- Confirm: The mean excess 7-bar return is positive with t ≥ 2, and the supporting check passes.
- Reject: The mean excess 7-bar return is negative with t ≤ -2.
- Inconclusive: The result is inconclusive in four cases: - t is between -2 and 2; - t ≥ 2 but the correlation is 0 or below; - fewer than 30 grid cases; - the cases fall on fewer than 30 distinct days.
