---
plan: 060-02.d1.d2.d2_volume-dry-up-longer-hold_1d
idea: 060-02.d1.d2.d2_volume-dry-up-longer-hold
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (20-bar forward return - coin mean 20-bar return) on grid cases: 0.023784; t of the mean, cases of one day pooled: 0.605475 (threshold: mean > 0 with t >= 2 (confirm), mean < 0 with t <= -2 (reject), from at least 30 cases)
- Supporting check: none
- Counts: grid cases with a non-zero forecast: 150, days: 54
- Decided by: The t lies between -2 and 2 (inconclusive rule).
- Reading: Situation taken as price-computed 20-day return < -10 % and 60-day return < -10 % (falling profile), falling back to regime == mean_reversion where a window lacks the history, with the expected side the sign of the raw log volume ratio; the coin's mean 20-bar return is taken over all windows' non-overlapping grid bars, the t is the day-clustered t of the case mean (per-day summed deviations), and fewer than 30 cases gives 'not observable' as the minimum-count rule.
- Size: unusual move +3.28 % (t 2.02, the cases of one day together: 200 days) per case over 20 bars, 0.164 of the coin's usual move (21.24 %); normal drift in its direction -0.28 %, total +2.99 %; 292 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d1.d2.d2_volume-dry-up-longer-hold_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d2.d2_volume-dry-up-longer-hold_1d`
Measure: `measure.py`
