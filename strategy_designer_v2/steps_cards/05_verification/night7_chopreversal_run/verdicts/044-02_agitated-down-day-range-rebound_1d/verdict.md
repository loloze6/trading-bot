---
plan: 044-02_agitated-down-day-range-rebound_1d
idea: 044-02_agitated-down-day-range-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x next-bar excess return over cases: 0.00575476; t, cases of one day together: 3.20737 (threshold: confirm: t >= 2 with wide-minus-narrow > 0; reject: t <= -2 or difference Welch t <= -2 (difference Welch t = 3.454))
- Supporting check: wide-minus-narrow mean next-bar excess return (split at coin median range multiple): 0.00644532, passed: True
- Counts: cases: 3752, distinct days: 1448
- Decided by: Confirm rule: main t (3.21) >= 2 and wide-minus-narrow difference (0.00645) > 0.
- Reading: Situation checked as close below the prior close within the window with a long forecast (the agitated profile is the code's added filter, not recomputable here; first bars of a window without a prior close left out); next-bar returns within windows; the coin's mean daily return is over all its windows' next-bar returns; the main t sums deviations per calendar day (clustered standard error); the range multiple is the recorded raw range_mult, the wider half being cases strictly above the coin's median and the narrower half at or below it; the plan's 'fewer cases -> inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.34 % (t 1.72, the cases of one day together: 1134 days) per case over 1 bars, 0.073 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.47 %; 2689 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004013 on the check folds against +0.005755 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/044-02_agitated-down-day-range-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/044-02_agitated-down-day-range-rebound_1d`
Measure: `measure.py`
