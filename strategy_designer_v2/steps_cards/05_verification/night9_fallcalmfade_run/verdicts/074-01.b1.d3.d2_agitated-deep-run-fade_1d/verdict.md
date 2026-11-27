---
plan: 074-01.b1.d3.d2_agitated-deep-run-fade_1d
idea: 074-01.b1.d3.d2_agitated-deep-run-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 1-day unusual move of cases (forecast <= -2), short direction: 0.0118082; t of the mean, cases of one day pooled: 2.49763 (threshold: positive with t >= 2 confirms (with supporting check); negative with t <= -2 rejects)
- Supporting check: mean unusual move top third minus bottom third of forecast size: 0.0164407, passed: True
- Counts: days with cases: 180, cases: 303
- Decided by: Mean unusual move positive with t >= 2 and the top-minus-bottom third check positive.
- Reading: Situation = an up close (close above previous close) ending a run of 2+ down closes, computed inside each window from prices, on the detector's mean_reversion regime (which carries the falling-agitated profile veto, not recomputable from the record), short side; active bars at a window start where the run length is unknown are left out; cases = bars with forecast <= -2 and a next close in the same window, the coin's mean daily return taken over all its windows, t from per-day summed deviations with a D/(D-1) correction, and thirds as the floor(n/3) smallest and largest |forecast| cases (ties ordered by day then coin); fewer than 30 days with cases is treated as not observable.
- Size: unusual move +1.18 % (t 2.50, the cases of one day together: 180 days) per case over 1 bars, 0.240 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +1.05 %; 303 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004715 on the check folds against +0.01181 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d2_agitated-deep-run-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d3.d2_agitated-deep-run-fade_1d`
Measure: `measure.py`
