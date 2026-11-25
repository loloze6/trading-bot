---
idea: 032-02_volatile-decline-low-rebound
brief: 032_monthly-low-in-volatile-decline
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: the coin fell over the past 30 days, its daily high-low ranges that month are wide against its past year, and it closes below the lowest low of the prior 30 days -> adapted: all three conditions are kept as a regime (30-day return < 0, 365/30 mean-bar-range ratio < 1, close below the prior 30-day low), and inside the regime the position is graded by how far the close sits below the prior low.
- Comparison: none -> kept
- Outcome: the price rises over the next 5 days, and rises more the further the close sits below the prior low -> kept: long for 5 bars, sized by the depth of the break.
- Verdict transfer: yes: the test measures exactly the stated conditions, direction, horizon and graded size, so its result carries over to the idea.
Forecast: The regime detector selects `mean_reversion` only when three things hold at the bar's close. First, the 30-day return is below 0. Second, the mean daily high-low range over the last 365 bars divided by the mean over the last 30 is below 1, which means this month's ranges are wider than the year's average. Third, the close sits below the lowest low of bars t-30..t-1. On every other bar the forecast is 0. Inside the regime, the forecast is the percent distance of the close below that prior 30-day low, standardised over 60 bars and then negated, so it is positive. It grows linearly with the depth of the break and is clipped at 0, so it is long only.
Config: 032-02_volatile-decline-low-rebound_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move over 5 bars after each case, compared with simply holding the coin. A case is a bet: a rise of the forecast of at least 2 points, read once per 5-bar grid cell. The unusual move is the case's 5-bar return minus the coin's normal 5-bar drift. Its t is computed with the cases of one day taken together.
- Supporting check: Across the cases, the least-squares slope of the unusual 5-bar move on the forecast at the case's bar is above 0. This tests that deeper breaks are followed by larger rises.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the slope check passes.
- Reject: The mean unusual move is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 when the slope is not above 0, and so is any result from fewer than 30 cases, whatever the t.
