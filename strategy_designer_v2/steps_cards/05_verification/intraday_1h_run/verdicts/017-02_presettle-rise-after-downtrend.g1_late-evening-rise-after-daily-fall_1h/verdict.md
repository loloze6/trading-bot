---
plan: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 21:00 excess 2-bar return on forecast, pooled: -6.27455e-05; OLS slope t: -3.72518 (threshold: slope t >= 2 to confirm (with supporting mean t >= 2); slope t <= -2 rejects)
- Supporting check: mean excess 2-bar return on 21:00 bars with forecast > 0: -7.46093e-05, passed: False
- Counts: days with forecast > 0 across coins: 8587, 21:00 cases: 17415
- Decided by: Reject rule met: slope t = -3.73, supporting mean t = -0.45 (one at -2 or lower).
- Reading: Cases are every bar stamped 21:00 UTC with a row two positions later in the same window (close[t+2] by row position), the coin mean is the mean 2-bar return on the non-overlapping grid of all its windows pooled, the slope t is the OLS slope over its standard error, the supporting check passes when its mean is above 0 with t >= 2, and the 300-day minimum counts 21:00 cases with forecast > 0 and a valid return, its shortfall giving 'not observable'.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h`
Measure: `measure.py`
