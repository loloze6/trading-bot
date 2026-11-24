---
plan: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
idea: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 24-bar excess return on forecast, settlement bars pooled: -5.69585e-05; OLS slope t: -0.646957 (threshold: slope > 0 with t >= 2 confirms (with check); slope < 0 with t <= -2 rejects)
- Supporting check: forecast-signed excess, top third minus bottom third by |forecast|: -0.00146457, passed: False
- Counts: settlement cases with a non-zero forecast: 1905
- Decided by: The slope's t lies between -2 and 2.
- Reading: Cases are settlement bars (start 23:00 UTC, close 00:00 UTC) with non-zero forecast and a full 24-bar forward return in-window; coin mean 24-bar return from the non-overlapping 0,24,48,... grid of all its windows; thirds are floor(n/3) cases each by |forecast| (stable sort); slope t = slope / its OLS standard error.
- Size: unusual move -0.08 % (t -0.57, the cases of one day together: 318 days) per case over 24 bars, -0.028 of the coin's usual move (3.25 %); normal drift in its direction +0.00 %, total -0.08 %; 1601 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h.md`
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_2026/backtests/017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h`
Measure: `measure.py`
