---
plan: 044-02_agitated-down-day-range-rebound_1d
idea: 044-02_agitated-down-day-range-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x next-bar excess return over cases: 0.00108866; t, cases of one day together: 0.215132 (threshold: confirm: t >= 2 with wide-minus-narrow > 0; reject: t <= -2 or difference Welch t <= -2 (difference Welch t = -0.574))
- Supporting check: wide-minus-narrow mean next-bar excess return (split at coin median range multiple): -0.00279935, passed: False
- Counts: cases: 406, distinct days: 178
- Decided by: Inconclusive rule: neither confirm nor reject met (main t 0.22, difference -0.002799, Welch t -0.57).
- Reading: Situation checked as close below the prior close within the window with a long forecast (the agitated profile is the code's added filter, not recomputable here; first bars of a window without a prior close left out); next-bar returns within windows; the coin's mean daily return is over all its windows' next-bar returns; the main t sums deviations per calendar day (clustered standard error); the range multiple is the recorded raw range_mult, the wider half being cases strictly above the coin's median and the narrower half at or below it; the plan's 'fewer cases -> inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.07 % (t 0.15, the cases of one day together: 137 days) per case over 1 bars, 0.047 of the coin's usual move (3.33 %); normal drift in its direction +0.06 %, total +0.13 %; 271 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/044-02_agitated-down-day-range-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2026/backtests/044-02_agitated-down-day-range-rebound_1d`
Measure: `measure.py`
