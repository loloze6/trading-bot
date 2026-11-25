---
plan: 034-01.d2_falling-agitated-low-close-rebound_1d
idea: 034-01.d2_falling-agitated-low-close-rebound
fit: exact
status: mismatch
---
Situation check: 52 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of nonzero-forecast bars are in-profile bars with the close nearer the low than usual and a long forecast
- Reading: The profile is read from the recorded regime (the only regime with a strategy, 'unknown', is the falling-agitated profile, the detector's components being unrecorded); the situation is close location (high-close)/(high-low) standardised above 10 recomputed in-window when 60 past bars exist (else the recorded post_pipeline value), on the long side; days are UTC calendar days of the bar timestamps, the coin mean is over all its bars' next-day returns across windows, and the plan's 100-day minimum is applied as 'not observable'.
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/034-01.d2_falling-agitated-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/034-01.d2_falling-agitated-low-close-rebound_1d`
Measure: `measure.py`
