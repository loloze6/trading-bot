---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: the coin's 30-day return is positive, more as it is larger -> kept: the 720-bar return, standardised and clipped at 0, so it is zero when that return is not positive.
- Comparison: the coin's usual 7-day drift, only in a year when its 1-year return is positive -> kept: a regime rule on the 8760-bar return being above 0, judged against holding the coin.
- Outcome: the coin rises over the next 7 days by more than its usual drift -> kept: a 168-bar hold, measured against the coin's mean 168-bar return.
- Verdict transfer: yes: the year condition, the graded 30-day rise and the 7-day excess rise are all measured as the idea states them.
Forecast: A regime rule makes the strategy active only while the coin's 8760-bar (1-year) return is above 0. On every other bar the forecast is 0 (flat). While the rule holds, the forecast is the coin's 720-bar (30-day) percent return, standardised against its past 500 values (min_periods 120) and clipped at 0. It is zero when the 30-day return is not positive, and otherwise positive and growing with the size of the 30-day rise, up to the cap of 20. It is long only and never negative.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h_config.json
Criterion:
- Horizon: 168 bars
- Main measure: The cases are bars on each window's non-overlapping 168-bar grid where the forecast is above 0. For each case, the unusual move is the coin's 168-bar return from that bar minus the coin's mean 168-bar return over all its windows (holding the coin). The measure is the mean unusual move with its t-statistic, before costs.
- Supporting check: Split the cases at the median forecast. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, over at least 100 independent cases, and the supporting check is above 0.
- Reject: The mean unusual move is below 0 with t ≤ -2, over at least 100 independent cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 whose supporting check is not above 0 is also inconclusive. So is any result from fewer than 100 independent cases.
