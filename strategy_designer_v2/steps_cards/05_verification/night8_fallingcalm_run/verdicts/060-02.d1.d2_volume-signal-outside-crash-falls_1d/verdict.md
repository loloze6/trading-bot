---
plan: 060-02.d1.d2_volume-signal-outside-crash-falls_1d
idea: 060-02.d1.d2_volume-signal-outside-crash-falls
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-5-bar excess return on forecast: 0.00117842; OLS slope t: 2.94895 (threshold: confirm: slope positive with t >= 2 and supporting check passes; reject: slope negative with t <= -2)
- Supporting check: book mean daily return minus market-rise gain (timing), before costs: 0.000271403, passed: True
- Counts: grid cases where the forecast is not 0: 599
- Decided by: The slope is positive with t >= 2 and the timing part is above 0.
- Reading: Situation = falling profile (60-bar return below -10 %, the config's veto) and 20-bar return in [-20 %, 0 %), recomputed from closes inside each window and checked on active bars where it is computable (the detector's regime is used only if none is), the expected side being the sign of the raw log volume ratio; the main measure is one pooled OLS of (5-bar return minus the coin's mean grid 5-bar return over all windows) on the forecast across all coins; the supporting check uses the before-cost book built from the held position times the next bar's return, each day averaged over coins.
- Size: unusual move +0.91 % (t 2.25, the cases of one day together: 523 days) per case over 5 bars, 0.087 of the coin's usual move (10.60 %); normal drift in its direction -0.13 %, total +0.78 %; 736 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001177 on the check folds against +0.001178 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d1.d2_volume-signal-outside-crash-falls_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d2_volume-signal-outside-crash-falls_1d`
Measure: `measure.py`
