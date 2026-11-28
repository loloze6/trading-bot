---
plan: 089-04_calm-decline-up-volume-lasting_1d
idea: 089-04_calm-decline-up-volume-lasting
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of the 10-bar excess return on the forecast (cases forecast > 0, day-clustered): -0.00172577; t of the OLS slope, day-clustered: -1.0793 (threshold: confirm: slope > 0 with t >= 2 and second-half check passes; reject: slope < 0 with t <= -2; at least 30 cases on at least 30 distinct days)
- Supporting check: forecast-weighted mean excess return over t+5 to t+10 > 0: -0.00557445, passed: False
- Counts: cases: 138, distinct days: 84
- Decided by: The slope has |t| < 2 (inconclusive rule). No effect (common/verdicts.md): t in the idea's direction -1.079 (below 1), 138 cases (30 needed).
- Reading: The falling calm profile is read from the recorded regime (the detector's 'unknown' regime, the one left when neither the trend veto nor the volatility veto fires) and the up side of the situation as the raw centred share > 0; the slope is the OLS slope of excess return on forecast with a day-clustered standard error; the coin's mean 10-bar return is the mean over the non-overlapping 10-bar grids of all its windows, and the second-half excess return is close[t+10]/close[t+5]-1 minus the coin's mean 5-bar return over the non-overlapping 5-bar grids of all its windows.
- Size: unusual move -0.86 % (t -0.95, the cases of one day together: 232 days) per case over 10 bars, -0.045 of the coin's usual move (16.20 %); normal drift in its direction +1.14 %, total +0.28 %; 277 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -1.079 (below 1), 138 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/089-04_calm-decline-up-volume-lasting_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/089-04_calm-decline-up-volume-lasting_1d`
Measure: `measure.py`
