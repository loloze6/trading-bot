---
plan: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d
idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of d = (scaled combined - scaled best) x excess 5-day return: 0.000475872; t of the mean: 0.281932 (threshold: confirm if t >= 2 with the check above 0; reject if t <= -2; at least 200 cases)
- Supporting check: mean d upper ret90 half minus lower half: 0.00573381, passed: True
- Counts: independent cases in the regime: 1704, active bars: 8785
- Decided by: The t of mean d lies between -2 and 2 (inconclusive rule).
- Reading: The idea claims no rise or fall, so the expected side on each active bar is the sign of the combined score, and the situation is ret90 > 0 (recorded value, else recomputed from prices inside the window); trending cases are bars with regime 'trending' at grid positions 0,5,10,... of each window with a full 5-bar forward return; each coin's mean 5-day return is taken over the same grid on all its windows' bars; the pooled standard deviations are taken over all cases of all coins; the median split puts ret90 above the median in the upper half and the rest in the lower half; the plan's 200-case minimum, when not met, gives 'not observable'.
- Size: unusual move -0.43 % per case over 5 bars, -0.039 of the coin's usual move (10.60 %); normal drift in its direction -0.08 %, total -0.51 %; 1571 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d`
Measure: `measure.py`
