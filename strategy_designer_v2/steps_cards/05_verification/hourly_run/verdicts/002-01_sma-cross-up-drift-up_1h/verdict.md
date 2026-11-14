---
plan: 002-01_sma-cross-up-drift-up_1h
idea: 002-01_sma-cross-up-drift-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 24-bar log return when forecast > 0 minus window mean over all bars, pooled: 0.000196106; t of the mean of excess over non-overlapping blocks: -0.435393 (threshold: excess > 0 with t >= 2 to confirm; excess < 0 with t <= -2 to reject)
- Supporting check: share of positive fwd 24-bar returns when forecast > 0 minus share over all bars: -0.0125398, passed: False
- Counts: non-overlapping 24-bar blocks with forecast above 0: 377
- Decided by: The main measure and the supporting check disagree in sign, so the result is inconclusive.
- Reading: The measure's value is the pooled mean excess over all forecast>0 bars (each demeaned by its own window's mean over all bars), its t is the ordinary one-sample t of that excess on greedy non-overlapping blocks that each start at the next forecast>0 bar after the previous block ends within a window, and the hit-rate shares are pooled across windows.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-01_sma-cross-up-drift-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-01_sma-cross-up-drift-up_1h`
Measure: `measure.py`
