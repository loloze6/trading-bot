---
plan: 031-02.b1.b2_flat-day-after-strong-rise_1d
idea: 031-02.b1.b2_flat-day-after-strong-rise
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move after a long case (day-pooled): 0.0332569; t of the mean, cases of one day pooled: 0.99587 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: OLS slope of unusual move on signal forecast > 0: 0.00490857, passed: True
- Counts: cases: 15, days: 15
- Decided by: Only 15 cases, fewer than the plan's 30, so the data cannot show the idea.
- Reading: Situation agreement is measured on active bars (forecast != 0) where the three rules can be computed (rise5 from its recorded raw value or else close/close[-5]-1, body |close-open|/(high-low) <= 0.1, range over the 20-row mean range including the day >= 1), leaving out active bars whose 20-day range history is not in the window; a case is the first long bet (forecast rise of >= 2 points from its low since the last bet, from 0 after flat) in each 10-row grid cell of a window, its unusual move is the 10-bar return from its close minus the coin's mean 10-bar return on the non-overlapping grid of all its windows, the t sums deviations per UTC day (clustered SE with D/(D-1) correction), and the plan's 'fewer than 30 cases' is applied as the minimum count.
- Size: unusual move +3.33 % (t 1.03, the cases of one day together: 15 days) per case over 10 bars, 0.180 of the coin's usual move (9.14 %); normal drift in its direction +0.71 %, total +4.04 %; 15 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b2_flat-day-after-strong-rise_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b2_flat-day-after-strong-rise_1d`
Measure: `measure.py`
