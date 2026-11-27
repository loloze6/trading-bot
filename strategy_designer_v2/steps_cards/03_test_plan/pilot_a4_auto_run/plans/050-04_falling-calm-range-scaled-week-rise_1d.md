---
idea: 050-04_falling-calm-range-scaled-week-rise
brief: 050_calm-downtrend-scaled-weeks-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: a coin that has risen over the last 7 days, in a falling calm market -> kept: the 7-day return, clipped at 0, so the book is flat when the coin has not risen; code adds the profile.
- Comparison: the 7-day rise in units of the coin's 30-day average daily high-low range -> kept: the return divided by the 30-day mean of (high - low) / close, graded.
- Outcome: the coin keeps rising over the next 3 days, further for larger scaled rises -> kept: long for 3 bars, sized by the scaled rise.
- Verdict transfer: yes
Forecast: The forecast is the 7-day return divided by the 30-day mean daily high-low range as a share of the close (MeanAbsScaledReturnComponent, period 7, window 30, base "mean_relative_range"). It is standardised against its own past 60 values, then clipped at 0. It is zero when the coin did not rise over 7 days. It is positive after a rise and grows linearly with the rise's size in usual daily ranges, capped at +20. It is never negative. The code's falling-calm profile keeps the book flat outside that profile.
Config: 050-04_falling-calm-range-scaled-week-rise_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Cases are bars on the non-overlapping 3-bar grid of each window where the forecast is above 0. For each case, take the coin's 3-day forward return minus the coin's mean 3-day return over all windows. The measure is the forecast-weighted mean of these excess returns. Its t is computed with cases of one day summed together.
- Supporting check: Split the cases at the median forecast. The mean excess return of the cases above the median minus that of the cases below it must be above 0.
- Confirm: The main measure is positive with t >= 2, and the supporting check passes.
- Reject: The main measure is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main measure with t >= 2 whose supporting check fails is also inconclusive. So is any result from fewer than 30 cases.
