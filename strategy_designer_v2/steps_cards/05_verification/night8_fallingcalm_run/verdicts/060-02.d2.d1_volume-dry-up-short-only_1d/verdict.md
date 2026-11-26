---
plan: 060-02.d2.d1_volume-dry-up-short-only_1d
idea: 060-02.d2.d1_volume-dry-up-short-only
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar short move per case (drift - return): 0.0131621; t of the mean, cases of one day summed: 2.5838 (threshold: confirm: mean > 0 with day-clustered t >= 2 over >= 30 cases and supporting difference > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual short move, larger |forecast| half minus smaller half (Welch difference): 0.0186013, passed: True
- Counts: cases: 472, days: 359
- Decided by: Mean unusual short move above 0 with t >= 2 over at least 30 cases, and larger-minus-smaller shrinkage difference above 0.
- Reading: Situation = regime 'mean_reversion' (falling-profile veto passed and 10-day return < 0), re-checked from prices (10-day return < 0, 60-day return < -10 %) where the window holds enough bars and raw volume log ratio < 0 where recorded; a case is the first short bet (rise of short forecast >= 2 points from its lowest level since the last bet) in each 5-bar grid cell with a full 5-bar return in the window; the day-clustered t uses a G/(G-1) correction; the split puts |forecast| > median in the larger half and <= median in the smaller.
- Size: unusual move +1.32 % (t 2.59, the cases of one day together: 359 days) per case over 5 bars, 0.123 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +0.73 %; 472 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01076 on the check folds against +0.01316 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d2.d1_volume-dry-up-short-only_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d2.d1_volume-dry-up-short-only_1d`
Measure: `measure.py`
