---
plan: 044-02_agitated-down-day-range-rebound_1d
idea: 044-02_agitated-down-day-range-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x next-bar excess return over cases: 0.00114121; t, cases of one day together: 0.21448 (threshold: confirm: t >= 2 with wide-minus-narrow > 0; reject: t <= -2 or difference Welch t <= -2 (difference Welch t = 0.854))
- Supporting check: wide-minus-narrow mean next-bar excess return (split at coin median range multiple): 0.00544081, passed: True
- Counts: cases: 452, distinct days: 276
- Decided by: Inconclusive rule: neither confirm nor reject met (main t 0.21, difference 0.005441, Welch t 0.85).
- Reading: Situation checked as close below the prior close within the window with a long forecast (the agitated profile is the code's added filter, not recomputable here; first bars of a window without a prior close left out); next-bar returns within windows; the coin's mean daily return is over all its windows' next-bar returns; the main t sums deviations per calendar day (clustered standard error); the range multiple is the recorded raw range_mult, the wider half being cases strictly above the coin's median and the narrower half at or below it; the plan's 'fewer cases -> inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.06 % (t 0.12, the cases of one day together: 213 days) per case over 1 bars, 0.025 of the coin's usual move (6.78 %); normal drift in its direction +0.84 %, total +0.90 %; 305 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/044-02_agitated-down-day-range-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/044-02_agitated-down-day-range-rebound_1d`
Measure: `measure.py`
