---
plan: 052-01_down-day-low-close-rebound_1d
idea: 052-01_down-day-low-close-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Welch t of next-day return, top minus bottom tercile of near_low on down days: 0.00407723; Welch t: 3.0325 (threshold: confirm: difference > 0 with Welch t >= 2 and supporting check passes; reject: Welch t <= -2, or top-tercile minus holding t <= -2)
- Supporting check: top tercile mean next-day return minus holding the coin (t: 3.802): 0.00367713, passed: True
- Counts: top tercile down-day cases: 2840, bottom tercile down-day cases: 2838
- Decided by: The top-minus-bottom difference is positive with a Welch t of 2 or more and the top tercile beats holding (confirm rule).
- Reading: Down days are recomputed as close[t] < close[t-1] inside each window (the regime column is used for a window's first bar only); terciles are taken per coin over all its windows on down-day bars (regime mean_reversion) having both near_low post_pipeline_value and a next-day return, ranked with ties broken by order; holding is the coin's mean next-day return over all its bars and windows, the supporting check is the mean of (top-tercile return minus its coin's holding) > 0 with its one-sample t used for the reject alternative; fewer than 300 cases in any tercile is reported as not observable.
- Size: unusual move +0.19 % (t 1.70, the cases of one day together: 1861 days) per case over 1 bars, 0.041 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.31 %; 6105 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.00203 on the check folds against +0.004077 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/052-01_down-day-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/052-01_down-day-low-close-rebound_1d`
Measure: `measure.py`
