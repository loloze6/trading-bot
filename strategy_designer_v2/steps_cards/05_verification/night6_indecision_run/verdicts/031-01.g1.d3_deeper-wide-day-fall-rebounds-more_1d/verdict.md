---
plan: 031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d
idea: 031-01.g1.d3_deeper-wide-day-fall-rebounds-more
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of position x (next-day return - coin mean daily return) over forecast>0 bars, same-day cases summed: 0.0192217; t of the mean of per-day summed cases: 2.93133 (threshold: confirm: mean > 0 with t >= 2 on >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 on >= 30 cases)
- Supporting check: Spearman(forecast, next-day excess return) > 0: 0.0130301, passed: True
- Counts: cases with a forecast above 0: 593, days: 289
- Decided by: Mean above 0 with t >= 2 on at least 30 cases and Spearman correlation above 0: the confirm rule.
- Reading: Range multiple uses the 20 recorded bars up to and including t within a window, so active bars without 20 prior bars are left out of the agreement share; the measure is position x (next-day return minus the coin's all-window mean daily return), the 30-case minimum counts (coin, bar) cases with forecast > 0, and the mean and t are taken over per-day sums of those cases.
- Size: unusual move +1.32 % (t 3.49, the cases of one day together: 284 days) per case over 1 bars, 0.265 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +1.44 %; 575 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d`
Measure: `measure.py`
