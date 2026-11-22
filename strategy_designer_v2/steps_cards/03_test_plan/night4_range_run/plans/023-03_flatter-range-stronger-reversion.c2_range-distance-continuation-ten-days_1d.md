---
idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the close's distance from the middle of its 30-day closing range -> kept
- Comparison: above versus below the middle of that range -> kept
- Outcome: the coin keeps moving the same way over the next 10 days -> kept
- Verdict transfer: yes: the forecast is the idea's own graded distance from the 30-day range middle, bet in its direction over its 10-day horizon.
Forecast: One DonchianBreakoutComponent with period 30 on closes. It measures where the close sits in its 30-day closing range: -1 at the low, 0 at the middle, +1 at the high. It is standardised over its own past 60 values. The forecast is positive (long) above the middle and negative (short) below it, and zero at the middle. Its size grows with the distance from the middle. No regime is used and there is no dead zone, because the idea is a steady relation rather than a condition.
Config: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Regress the coin's 10-bar forward return on the forecast, pooled over coins, at grid bars 0, 10, 20, ... of each window. The forward return has the coin's mean 10-bar return over all windows removed. The measure is the t of the slope.
- Supporting check: The book's mean daily return minus its gain from the market's own rise (the timing part) is above 0.
- Confirm: The slope t is 2 or more and the timing part is positive.
- Reject: The slope t is -2 or less, meaning moves away from the middle reverse.
- Inconclusive: A slope t between -2 and 2, or t of 2 or more with a timing part of 0 or less. At least 300 non-overlapping cases are needed (about 1,700 expected); with fewer, the result is inconclusive.
