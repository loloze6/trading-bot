---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising
fit: adapted
status: inconclusive
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next 5-bar excess return on forecast (non-overlapping grid): 0.000668681; OLS slope t: 1.89754 (threshold: confirm: t >= 2 with timing gain > 0; reject: t <= -2; else inconclusive; at least 200 grid cases with non-zero forecast)
- Supporting check: book timing gain before costs (mean daily): 0.000207673, passed: True
- Counts: grid cases with a non-zero forecast: 3419, grid cases: 3419
- Decided by: The slope's t is between -2 and 2.
- Reading: The situation is rebuilt as the sign of the mean of the three standardised components (from raw values, using the recorded post-pipeline value where a window's own history is too short); the slope uses every grid bar (zero forecasts included) while the minimum count is the grid bars with non-zero forecast; the timing gain uses the before-cost position gain, allocation x next bar return, averaged over coins per day; fewer than 200 cases gives 'not observable' per the workflow rule.
- Size: unusual move +0.43 % per case over 5 bars, 0.034 of the coin's usual move (10.60 %); normal drift in its direction +0.04 %, total +0.47 %; 1894 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d`
Measure: `measure.py`
