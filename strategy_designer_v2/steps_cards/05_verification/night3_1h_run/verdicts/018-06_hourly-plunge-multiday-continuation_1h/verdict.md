---
plan: 018-06_hourly-plunge-multiday-continuation_1h
idea: 018-06_hourly-plunge-multiday-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: ordinary t of mean strength of short cases over 120 bars (drift-adjusted, per usual 120-bar move): 0.000656589; ordinary t of the mean: 0.03708 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: Spearman of |forecast| at signal bar vs strength > 0: -0.0139977, passed: False
- Counts: cases: 3165, active bars: 202702
- Decided by: t between -2 and 2 over at least 30 cases.
- Reading: The situation is a negative 24-bar return with a short forecast; a case is a deepening of the short forecast by at least 2 points from its shallowest level since the last bet (reset at flat), first one per 120-bar grid cell from each window's first row, dropped if its 120-bar return leaves the window; drift and usual move are the mean and sample std of each coin's non-overlapping 120-bar returns pooled over windows; fewer than 30 cases gives not observable per the workflow's minimum-count rule.
- Size: unusual move -0.02 % per case over 120 bars, 0.001 of the coin's usual move (10.37 %); normal drift in its direction -0.65 %, total -0.67 %; 3165 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation_1h`
Measure: `measure.py`
