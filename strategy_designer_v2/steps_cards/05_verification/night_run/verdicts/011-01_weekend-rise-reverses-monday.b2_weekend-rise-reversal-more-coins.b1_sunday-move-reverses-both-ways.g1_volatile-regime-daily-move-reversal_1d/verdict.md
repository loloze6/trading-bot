---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean next-day timing gain: position x (next return - coin's mean daily return), before costs: 0.000452397; ordinary t of the mean: 3.11184 (threshold: confirm: mean > 0 with ordinary t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2)
- Supporting check: per-unit-|position| timing gain, top third minus bottom third by |position|: 0.000899915, passed: True
- Counts: non-zero-position bars: 36021, bars in main measure: 36106
- Decided by: The main mean is positive with t >= 2 and the top-minus-bottom per-unit gain is positive.
- Reading: The main mean pools every bar with a position and a next close in the same window, zero positions included. The supporting check ranks only the non-zero-position bars into thirds by |position| and measures each third's gain per unit as sum(gain)/sum(|position|). The plan's 'else inconclusive' minimum of 1000 non-zero-position bars is applied as 'not observable', as the workflow requires.
- Size: unusual move +0.12 % per case over 1 bars, 0.025 of the coin's usual move (5.32 %); normal drift in its direction +0.00 %, total +0.12 %; 23115 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d`
Measure: `measure.py`
