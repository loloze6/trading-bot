---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 10-bar excess forward return on forecast (trending grid bars): 0.0028654; OLS slope t: 3.18406 (threshold: confirm needs t >= 2 (with check negative, t <= -2); reject if t <= -2 (or check positive, t >= +2))
- Supporting check: mean excess return s>=14 minus 8<=s<14 (Welch t) (t=-0.382): -0.00946034, passed: False
- Counts: non-overlapping cases (main): 833, cases with s >= 14: 248, cases with 8 <= s < 14: 110
- Decided by: Inconclusive rule: enough cases, but neither confirm (slope t >= 2 with check t <= -2) nor reject (slope t <= -2 or check t >= +2) holds.
- Reading: Situation is regime == 'trending' and expected side is the sign of the graded shape of s (run's standardised value); the coin's mean 10-bar return is taken over all grid bars of all its windows; a tier below 20 cases is treated as a minimum count not reached (not observable).
- Size: unusual move +2.68 % per case over 10 bars, 0.164 of the coin's usual move (14.49 %); normal drift in its direction +0.36 %, total +3.04 %; 815 cases
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d`
Measure: `measure.py`
