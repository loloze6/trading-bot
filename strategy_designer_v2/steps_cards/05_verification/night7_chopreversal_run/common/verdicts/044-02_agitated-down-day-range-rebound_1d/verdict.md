---
plan: 044-02_agitated-down-day-range-rebound_1d
idea: 044-02_agitated-down-day-range-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x next-bar excess return over cases: 0.00403837; t, cases of one day together: 2.50997 (threshold: confirm: t >= 2 with wide-minus-narrow > 0; reject: t <= -2 or difference Welch t <= -2 (difference Welch t = 5.177))
- Supporting check: wide-minus-narrow mean next-bar excess return (split at coin median range multiple): 0.00599661, passed: True
- Counts: cases: 10012, distinct days: 2226
- Decided by: Confirm rule: main t (2.51) >= 2 and wide-minus-narrow difference (0.00600) > 0.
- Reading: Situation checked as close below the prior close within the window with a long forecast (the agitated profile is the code's added filter, not recomputable here; first bars of a window without a prior close left out); next-bar returns within windows; the coin's mean daily return is over all its windows' next-bar returns; the main t sums deviations per calendar day (clustered standard error); the range multiple is the recorded raw range_mult, the wider half being cases strictly above the coin's median and the narrower half at or below it; the plan's 'fewer cases -> inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.20 % (t 1.18, the cases of one day together: 1773 days) per case over 1 bars, 0.040 of the coin's usual move (5.12 %); normal drift in its direction +0.12 %, total +0.32 %; 6823 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/044-02_agitated-down-day-range-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/common/backtests/044-02_agitated-down-day-range-rebound_1d`
Measure: `measure.py`
