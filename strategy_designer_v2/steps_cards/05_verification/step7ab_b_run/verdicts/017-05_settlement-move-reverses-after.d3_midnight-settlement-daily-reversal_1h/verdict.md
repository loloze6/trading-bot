---
plan: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
idea: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 24-bar excess return on forecast, settlement bars pooled: 0.000151817; OLS slope t: 4.51304 (threshold: slope > 0 with t >= 2 confirms (with check); slope < 0 with t <= -2 rejects)
- Supporting check: forecast-signed excess, top third minus bottom third by |forecast|: 0.00246277, passed: True
- Counts: settlement cases with a non-zero forecast: 17002
- Decided by: The slope is positive with t >= 2 and the top-minus-bottom third check is above 0.
- Reading: Cases are settlement bars (start 23:00 UTC, close 00:00 UTC) with non-zero forecast and a full 24-bar forward return in-window; coin mean 24-bar return from the non-overlapping 0,24,48,... grid of all its windows; thirds are floor(n/3) cases each by |forecast| (stable sort); slope t = slope / its OLS standard error.
- Size: unusual move +0.14 % per case over 24 bars, 0.030 of the coin's usual move (4.87 %); normal drift in its direction -0.01 %, total +0.13 %; 14568 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h.md`
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h`
Measure: `measure.py`
