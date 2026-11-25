---
plan: 039-01.d1_falling-agitated-low-close-rebound_1d
idea: 039-01.d1_falling-agitated-low-close-rebound
fit: exact
status: mismatch
---
Situation check: 50 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the active bars are in-profile bars with the close low in its range and a long forecast: the config also takes positions (short or long) where the plan's situation on its long side does not hold.
- Reading: The plan's situation is read as regime not 'chop' (the profile, as the detector decided it) and the close in the lower half of the day's range ((high-close)/(high-low) >= 0.5), on the long side; the coin's mean daily return is the mean of all its 1-bar returns over all windows, and days are UTC calendar days of the bar's timestamp.
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/039-01.d1_falling-agitated-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/039-01.d1_falling-agitated-low-close-rebound_1d`
Measure: `measure.py`
