---
plan: N2-05_shock-up-continuation_1d
idea: N2-05_shock-up-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar excess return after forecast>=10 events: 0.00875825; t of the mean: 1.66608 (threshold: confirm if mean > 0 and t >= 2, reject if mean < 0 and t <= -2, over at least 30 independent events)
- Supporting check: mean next-bar excess return after events, expected |t| < 2: -0.00196227, passed: True
- Counts: independent events: 601
- Decided by: With at least 30 independent events, the t of the mean 5-bar excess return lies between -2 and 2.
- Reading: Events merge when within 5 bars (difference <= 5) of the previous counted event in the same window, counted events without a bar t+5 in their window are left out of the measure, the coin's mean daily return is the mean of all within-window one-bar returns, and the supporting check is reported but does not gate the verdict since the confirm rule does not mention it.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N2-05_shock-up-continuation_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-05_shock-up-continuation_1d`
Measure: `measure.py`
