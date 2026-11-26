---
plan: 039-02_agitated-range-fall-low-close-rebound_1d
idea: 039-02_agitated-range-fall-low-close-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return on forecast > 0 bars: 0.00337211; t of weighted mean, same-day cases summed (day-clustered): 1.41614 (threshold: above 0 with t >= 2 (confirm, with supporting check); below 0 with t <= -2 (reject))
- Supporting check: top-half minus bottom-half mean excess return by forecast: 0.0031638, passed: True
- Counts: distinct days with forecast > 0: 1096, cases (coin-bars with forecast > 0): 3444
- Decided by: t lies between -2 and 2.
- Reading: Every bar is on the 1-bar grid; the coin's mean daily return is over all its windows; the t sums each day's weighted deviations into one piece (day-clustered standard error); halves are the n//2 lowest and n//2 highest forecasts (middle case dropped if odd), unweighted means; the 100-day minimum counts distinct UTC days with a forecast > 0 case that has a next-day return.
- Size: unusual move +0.06 % (t 0.26, the cases of one day together: 834 days) per case over 1 bars, 0.011 of the coin's usual move (5.40 %); normal drift in its direction +0.15 %, total +0.21 %; 2278 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/039-02_agitated-range-fall-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_coins/backtests/039-02_agitated-range-fall-low-close-rebound_1d`
Measure: `measure.py`
