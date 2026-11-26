---
plan: 032-01_calm-decline-depth-continues_1d
idea: 032-01_calm-decline-depth-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next 5-bar excess return on the forecast (forecast < 0 cells): 0.000401883; slope t, day-clustered: 0.351918 (threshold: confirm: slope > 0 with t >= 2 and short-direction mean excess > 0; reject: slope < 0 with t <= -2, or short-direction mean t <= -2; fewer than 30 independent days: inconclusive)
- Supporting check: mean short-direction excess 5-bar return > 0 (t summed per day: -0.065): -0.000521782, passed: False
- Counts: independent days of cases: 141, cases (coin-cells with forecast < 0): 173
- Decided by: Inconclusive rule: the slope's t lies between -2 and 2 (or cannot be computed) and no reject rule is met.
- Reading: Calm is read from the recorded regime 'trending' and the fall from fall28's raw value (28-bar price return where not recorded); the slope is pooled OLS of excess return on forecast with its t from a day-clustered standard error (case terms summed per day, G/(G-1) correction), the short-direction mean's t sums its deviations per day, the coin's mean 5-bar return is over its non-overlapping grid cells of all windows, and the 30-day minimum (stated as inconclusive by the plan) is applied as the minimum count, i.e. 'not observable'.
- Size: unusual move +0.29 % (t 0.41, the cases of one day together: 178 days) per case over 5 bars, 0.019 of the coin's usual move (10.60 %); normal drift in its direction -0.61 %, total -0.32 %; 190 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-01_calm-decline-depth-continues_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-01_calm-decline-depth-continues_1d`
Measure: `measure.py`
