---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean |forecast|/10-weighted short gain over coin drift, 5-bar grid cases with forecast <= -2: 0.00673087; t of the mean: 1.49951 (threshold: t >= 2 confirms (with >= 30 cases and supporting check > 0); t <= -2 rejects (with >= 30 cases))
- Supporting check: mean excess fall of above-median |forecast| cases minus below-median cases: -0.00395413, passed: False
- Counts: cases: 699
- Decided by: A t between -2 and 2 is inconclusive.
- Reading: Cases are grid bars (positions 0,5,10,... of each window) with forecast <= -2 and a 5-bar return inside the window, the coin's mean 5-bar return is over the same grid across all its windows, each case's value is -(excess return) x |forecast|/10 and the t is the ordinary t of their mean; the supporting check uses unweighted excess falls with cases equal to the median left out; and for the situation check, the 20-day return is taken from prices, or from the recorded regime on a window's first 20 bars.
- Size: unusual move +1.22 % per case over 5 bars, 0.101 of the coin's usual move (11.11 %); normal drift in its direction -0.72 %, total +0.50 %; 691 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends_1d`
Measure: `measure.py`
