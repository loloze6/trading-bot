---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: drift-removed 5-bar fall after shorts, weighted by abs(forecast)/mean abs(forecast): 0.00712926; t of the mean: 1.69572 (threshold: confirm: mean > 0 with t >= 2 and slope < 0; reject: mean < 0 with t <= -2; min 100 non-overlapping cases)
- Supporting check: least-squares slope of drift-removed 5-bar return on abs(forecast): 0.000413085, passed: False
- Counts: non-overlapping cases: 1031, active bars: 5167
- Decided by: t lies between -2 and 2
- Reading: situation = raw excess_power > 0 and 20-day return (recomputed from closes, else regime) < 0, side short; cases are grid bars 0,5,10,... of each window with forecast < 0 and a full 5-bar return inside the window, drift = the coin's mean 5-bar grid return over all its windows, t = ordinary t of the mean of weighted values
- Size: unusual move +1.21 % per case over 5 bars, 0.100 of the coin's usual move (11.16 %); normal drift in its direction -0.71 %, total +0.50 %; 698 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d`
Measure: `measure.py`
