---
plan: 032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop_1d
idea: 032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of demeaned 7-bar forward return on forecast, pooled: 0.000970546; OLS slope t: 3.55922 (threshold: confirm: slope > 0 with t >= 2 and timing > 0; reject: slope < 0 with t <= -2)
- Supporting check: timing part of mean daily book return before costs: 0.000524129, passed: True
- Counts: grid cases with a non-zero forecast: 1889
- Decided by: The slope is positive with t >= 2 and the timing part is above 0.
- Reading: Active bars whose 30-day efficiency ratio cannot be computed inside their window (first 30 bars) are left out of the agreement share; the expected side is the sign of the raw scaled 7-day move (continuation); the coin's mean 7-bar return is the mean over all its windows' grid returns; the timing part is the mean daily (per-day mean over coins) of position x (coin's daily return minus its mean daily return over all windows), before costs; fewer than 100 grid cases gives 'not observable'.
- Size: unusual move +0.50 % (t 1.32, the cases of one day together: 1091 days) per case over 7 bars, 0.035 of the coin's usual move (12.44 %); normal drift in its direction -0.01 %, total +0.49 %; 2101 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002274 on the check folds against +0.0009705 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop_1d`
Measure: `measure.py`
