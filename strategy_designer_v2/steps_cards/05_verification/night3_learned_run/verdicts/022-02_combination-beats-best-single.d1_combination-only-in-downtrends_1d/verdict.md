---
plan: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d
idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of (zc - zb) x r on decline grid cases: None (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive; at least 100 grid cases)
- Supporting check: deeper-half mean minus shallower-half mean of (zc - zb) x r: None, passed: None
- Counts: grid cases on decline bars: 0
- Decided by: Fewer than 100 grid cases on decline bars with both scores and the forward return (the best-single composite needs 365-bar histories inside a window), so the plan's minimum is not reached.
- Reading: The expected side is the sign of the combined score (forecast sign = sign of combo's raw value); the 90-day return is close[t]/close[t-90]-1 inside the window, with the recorded regime used where the window has fewer than 90 prior bars; 'best' weighting = the z-scored signal with the largest absolute past 365-bar correlation to the 5-bar forward return, signed by that correlation, needing full 365-bar windows inside one window; standard deviations use ddof=1 over the cases used; the deeper half is 90-day return below the median, the shallower half at or above it; cases with any missing value are left out.
- Size: unusual move -0.11 % per case over 5 bars, -0.006 of the coin's usual move (10.60 %); normal drift in its direction +0.02 %, total -0.09 %; 1423 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d`
Measure: `measure.py`
