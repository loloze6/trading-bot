---
plan: 058-01.g2.d1_volume-dry-up-at-the-lows_1d
idea: 058-01.g2.d1_volume-dry-up-at-the-lows
fit: exact
status: mismatch
---
Situation check: 73 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the active bars are short bars in the falling calm profile with volume shrunk (raw log ratio < 0): the config shorts also where the plan's situation (volume shrunk near the low) does not hold.
- Reading: The falling calm profile is read as regime 'unknown' (the regime holding the strategy, the vetoes sending other bars to chop), 'volume shrunk' as a raw vol_shrink log ratio below 0, and nearness to the low as graded (no cut-off) as the Fidelity says it is damped; the top/bottom halves are the largest and smallest floor(n/2) cases by |forecast| (the middle case dropped when n is odd); the day-clustered t of the weighted mean uses the per-day sums of w*(x-mean) with a G/(G-1) correction; and fewer than 30 cases or 20 days is reported as not observable.
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-01.g2.d1_volume-dry-up-at-the-lows_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.g2.d1_volume-dry-up-at-the-lows_1d`
Measure: `measure.py`
