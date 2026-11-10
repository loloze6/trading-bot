---
plan: 002-01_sma-cross-up-drift-up_1h
idea: 002-01_sma-cross-up-drift-up
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: forward 24-bar log return when forecast > 0 minus window mean over all bars: 0.000196106; one-sample t of mean excess on non-overlapping 24-bar blocks: -0.435393 (threshold: confirm if excess > 0 with t >= 2; reject if excess < 0 with t <= -2)
- Supporting check: hit rate when forecast > 0 minus hit rate over all bars: -0.0125398, passed: False
- Counts: non-overlapping 24-bar blocks with forecast above 0: 377, bars with forecast above 0: 8283
- Decided by: Inconclusive: the t-statistic lies between -2 and 2.
- Reading: The main measure's value is the mean, over all pooled bars with forecast > 0, of each bar's forward 24-bar log return minus its window's mean over all bars. Its t is the ordinary one-sample t of the same excess on greedy non-overlapping blocks, each started at the next bar with forecast > 0 and then skipping 24 bars. The hit-rate shares are pooled across windows. A reject also needs a supporting check that is not positive.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-01_sma-cross-up-drift-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-01_sma-cross-up-drift-up_1h`
Measure: `measure.py`
