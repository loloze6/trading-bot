---
plan: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d
idea: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean short-direction 2-bar unusual move: 0.000941352; t of the weighted mean: 0.396295 (threshold: t >= 2 over at least 30 cases confirms (with supporting check); t <= -2 over at least 30 cases rejects)
- Supporting check: mean unusual move, larger abs(forecast) half minus smaller half: -0.006095, passed: False
- Counts: cases: 833
- Decided by: The main measure's t lies between -2 and 2 over at least 30 cases.
- Reading: Regime recomputed from prices where 90 bars of window history exist, else the recorded regime; a rise is a positive raw vol-scaled 1-day return; a case is the first short bet (forecast falling by >= 2 points from its lowest short level since the last bet, from 0 after flat) in each 2-bar grid cell from the window's first row; drift is the coin's mean 2-bar return on that grid over all windows; the t of the weighted mean uses the weighted standard error sqrt(sum w^2 (v-m)^2)/sum w x sqrt(n/(n-1)); the median split puts abs(forecast) >= median in the larger half and < median in the smaller, halves compared by unweighted means.
- Size: unusual move +0.22 % per case over 2 bars, 0.038 of the coin's usual move (6.58 %); normal drift in its direction -0.24 %, total -0.02 %; 833 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d`
Measure: `measure.py`
