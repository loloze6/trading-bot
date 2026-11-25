---
plan: 032-02.g1.b1_uptrend-near-high-more-coins_1d
idea: 032-02.g1.b1_uptrend-near-high-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-day return, top third minus bottom third of forecast: 0.00658058; Welch t: 0.941376 (threshold: confirm: difference > 0 with Welch t >= 2 and top third mean excess > 0; reject: difference < 0 with Welch t <= -2)
- Supporting check: top third mean excess 5-day return > 0: 0.0105238, passed: True
- Counts: cases in trending regime: 3537, top third cases: 1179, bottom third cases: 1179
- Decided by: Welch t lies between -2 and 2.
- Reading: Situation = 28-bar close-to-close return > 0 recomputed from closes inside the window (the detector's 'trending' regime on the first 28 bars where it cannot be recomputed), long side, with a positive recorded high proximity; cases = bars with regime 'trending' at grid positions 0,5,10,... of each window with a 5-bar forward return inside the window; normal drift = mean of the coin's non-overlapping 5-bar returns over all its windows; thirds = pooled cases sorted by forecast (stable sort), bottom and top floor(n/3) cases; a third below 30 cases is 'not observable'.
- Size: unusual move +1.05 % (t 2.52, the cases of one day together: 1153 days) per case over 5 bars, 0.076 of the coin's usual move (12.35 %); normal drift in its direction +0.80 %, total +1.85 %; 2944 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.b1_uptrend-near-high-more-coins_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.b1_uptrend-near-high-more-coins_1d`
Measure: `measure.py`
