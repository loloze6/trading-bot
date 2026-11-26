---
plan: 039-02_agitated-range-fall-low-close-rebound_1d
idea: 039-02_agitated-range-fall-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return on forecast > 0 bars: 0.00543445; t of weighted mean, same-day cases summed (day-clustered): 2.75958 (threshold: above 0 with t >= 2 (confirm, with supporting check); below 0 with t <= -2 (reject))
- Supporting check: top-half minus bottom-half mean excess return by forecast: 0.00640905, passed: True
- Counts: distinct days with forecast > 0: 1449, cases (coin-bars with forecast > 0): 3753
- Decided by: Weighted mean excess return above 0 with t >= 2 and the top-minus-bottom-half check above 0.
- Reading: Every bar is on the 1-bar grid; the coin's mean daily return is over all its windows; the t sums each day's weighted deviations into one piece (day-clustered standard error); halves are the n//2 lowest and n//2 highest forecasts (middle case dropped if odd), unweighted means; the 100-day minimum counts distinct UTC days with a forecast > 0 case that has a next-day return.
- Size: unusual move +0.35 % (t 1.80, the cases of one day together: 1078 days) per case over 1 bars, 0.078 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.47 %; 2506 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003035 on the check folds against +0.005434 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/039-02_agitated-range-fall-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/039-02_agitated-range-fall-low-close-rebound_1d`
Measure: `measure.py`
