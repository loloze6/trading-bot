---
plan: 023-02_flat-range-bottom-reverts-up_1d
idea: 023-02_flat-range-bottom-reverts-up
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return of cases with forecast > 0 (minus coin's normal 5-bar drift): -0.0049706; t of the mean: -1.25258 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; fewer than 30 independent cases is inconclusive/not observable)
- Supporting check: mean excess return of larger-forecast half minus smaller-forecast half: 0.00664189, passed: True
- Counts: independent cases: 628, active bars: 3238
- Decided by: t lies between -2 and 2 (or could not be computed).
- Reading: Situation is taken as regime == 'mean_reversion' (the detector's recorded decision for NMR(30) <= 0.3) and raw below_mid value < 0 (close below the 30-bar midpoint), long side; the forecast halves split the cases sorted by forecast into the top and bottom floor(n/2), dropping the middle case when n is odd; normal drift is the mean of the coin's non-overlapping 5-bar grid returns over all its windows.
- Size: unusual move -0.61 % per case over 5 bars, -0.057 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total -0.02 %; 926 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-02_flat-range-bottom-reverts-up_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-02_flat-range-bottom-reverts-up_1d`
Measure: `measure.py`
