---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar return on forecast<0 bars minus mean next-bar return on all bars (BTC, pooled windows): -0.0578031; stretch-clustered t: -0.312946 (threshold: in-state mean at least 0.10% per day below the all-bars mean with stretch-clustered t <= -2 (confirm); difference >= 0 (reject))
- Supporting check: share of down bars in stretches minus share over all bars: -0.000439188, passed: False
- Counts: distinct down-cross stretches: 5, in-state bars pooled: 434
- Decided by: The difference is negative but t > -2, or it is smaller than 0.10% per day, or the down-bar share inside the stretches is not higher, so the confirm rule is not met.
- Reading: In-state bars are bars with forecast < 0 and a next-bar return inside the window; a stretch is a maximal run of consecutive forecast<0 bars within one window; the t is the in-state-minus-all-bars difference over the stretch-clustered (CR1, G/(G-1)) standard error of the in-state mean, treating the all-bars mean as the reference; the supporting check's pass is the down-bar share comparison the confirm rule names.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`
