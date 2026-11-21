---
plan: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d
idea: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day excess return on forecast: 0.000355971; OLS slope t: 6.61628 (threshold: slope t >= 2 confirms (with supporting check); t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean next-day excess return on bars with forecast > 0: 0.0016162, passed: True
- Counts: bars with forecast > 0: 8513, bars: 17380
- Decided by: The slope's t is 2 or more and the mean next-day excess return on forecast > 0 bars is above 0.
- Reading: The 300-bar minimum is counted on forecast > 0 bars that have a next-day return inside their window, and a shortfall is reported as 'not observable' per the workflow; the slope's t is the ordinary OLS t over every pooled bar, with the coin mean taken over all its windows' 1-bar returns.
- Size: unusual move +0.24 % per case over 1 bars, 0.048 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.36 %; 4653 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d`
Measure: `measure.py`
