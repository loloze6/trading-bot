---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of (forecast/10) x (5-bar return minus coin's mean 5-bar return), short grid bars: 0.0162631; t of the mean: 3.68442 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 grid cases)
- Supporting check: none
- Counts: grid cases: 374
- Decided by: The mean product is positive with t >= 2 over at least 30 grid cases.
- Reading: The grid is each window's bars 0, 5, 10, ... that have a close 5 bars later. The coin's mean 5-bar return is taken on that same grid over all its windows. The plan's 'fewer than 30 grid cases' is read as the minimum count, which gives 'not observable'. Before 20 bars of a window exist, the recorded regime stands in for the return gate in the situation check.
- Size: unusual move +1.45 % per case over 5 bars, 0.120 of the coin's usual move (11.11 %); normal drift in its direction -0.68 %, total +0.77 %; 528 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces_1d`
Measure: `measure.py`
