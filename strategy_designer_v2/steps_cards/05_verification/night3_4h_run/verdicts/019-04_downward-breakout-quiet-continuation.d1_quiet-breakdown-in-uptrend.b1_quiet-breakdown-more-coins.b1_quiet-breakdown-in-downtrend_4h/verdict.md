---
plan: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of short bets, short direction: 0.00375184; t of the mean: 2.67017 (threshold: mean > 0 with t >= 2 over at least 30 cases (reject: mean < 0 with t <= -2))
- Supporting check: mean unusual move, larger |forecast| half minus smaller half: None, passed: None
- Counts: cases: 4087, larger half: 0, smaller half: 4087
- Decided by: t >= 2 but the supporting check (larger |forecast| half minus smaller half > 0) fails.
- Reading: Situation = close below the prior 12-bar low (component raw value > 0, else from prices) and 180-bar close-to-close return < 0 recomputed within each window, short side; active bars where either cannot be computed (first 180 bars of a window) are left out of the agreement; a case is the first short bet (forecast falling >= 2 points below its least-negative level since the last bet, reset to 0 after flat or side change) in each 18-bar grid cell from each window's first row; the larger half is |forecast| strictly above the median, the smaller half at or below it.
- Size: unusual move +0.38 % per case over 18 bars, 0.034 of the coin's usual move (9.29 %); normal drift in its direction -0.52 %, total -0.14 %; 4087 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h`
Measure: `measure.py`
