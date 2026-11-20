---
plan: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h
idea: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 2-bar excess return on forecast at 20:00-stamped bars: 4.54146e-05; OLS slope t: 2.77703 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 2-bar return above median positive forecast: 0.00122311, passed: True
- Counts: decision bars: 17403, decision bars with a positive forecast: 8613, decision bars above the median positive forecast: 4306
- Decided by: The slope is positive with t >= 2 and the supporting check passes.
- Reading: The situation is bars whose next bar starts at 21:00 or 22:00 UTC with a negative raw 24-bar vol-scaled return and a positive forecast. The regression pools all coins' 20:00-stamped decision bars, including those with a zero forecast. Each coin's mean 2-bar return is taken on the non-overlapping grid 0,2,4,... of every window, pooled across windows. A shortfall from the 300-case minimum is reported as 'not observable'.
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h`
Measure: `measure.py`
