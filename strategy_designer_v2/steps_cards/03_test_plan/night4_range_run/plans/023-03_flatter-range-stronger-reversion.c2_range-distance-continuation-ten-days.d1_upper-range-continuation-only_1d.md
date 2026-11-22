---
idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 10d8cbead801
---
Fidelity:
- Situation: the daily close sits above the middle of its 30-day closing range, the farther the stronger -> kept
- Comparison: the middle of the 30-day closing range -> kept
- Outcome: the coin keeps rising over the next 10 days, more the farther above the middle; no mirror short -> kept
- Verdict transfer: yes: the forecast is the close's graded position above the 30-day closing-range middle, held 10 days, long only, as the idea states.
Forecast: The forecast uses DonchianBreakoutComponent with period 30, reading closes only. It gives the close's position in its 30-day closing range: 0 at the middle, rising continuously to the top. It is standardised over its past 60 values and clipped at 0. It is zero at or below the middle of the range, so there is never a short. It grows linearly as the close nears the top of the range, up to the cap of 20.
Config: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window, bars with forecast > 0 only. Fit the slope of the coin's 10-bar forward return, minus the coin's mean 10-bar return over all windows, on the forecast. The data are pooled over coins and windows; report the slope and its t.
- Supporting check: On the same grid, the mean excess 10-bar return (forward return minus the coin's mean 10-bar return) of the cases with forecast > 0 must be above 0.
- Confirm: The slope is positive with t >= 2 and the supporting check's mean excess return is above 0.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive. So is a positive slope with t >= 2 whose mean excess return is not above 0. Fewer than 100 grid cases with forecast > 0 is also inconclusive.
