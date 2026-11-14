---
plan: N2-06_rebound-in-high-volatility_1d_oos
idea: N2-06_rebound-in-high-volatility
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: net up-share high-vol minus quiet, top-decile drops: 0.0534119; two-proportion z: 1.91244 (threshold: confirm if z >= 2 (high-vol share above quiet), reject if z <= -2, otherwise inconclusive)
- Supporting check: mean next-bar return net of coin mean, high-vol top-decile drops (t): 0.00485555, passed: False
- Counts: high_volatility_top_decile_drop_bars: 671, quiet_top_decile_drop_bars: 610
- Decided by: z lies between -2 and 2, which the plan calls inconclusive.
- Reading: Top 10 percent means forecast at or above the 90th percentile of all bars' forecasts pooled (and positive); high-volatility bars are those the detector labelled 'trending' (volp >= 0.5), quiet bars the rest; the z-test uses the difference of coin-netted shares over the pooled raw-share standard error; the supporting check passes when its one-sample t is >= 2; fewer than 30 bars in a group gives 'not observable'.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N2-06_rebound-in-high-volatility_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N2-06_rebound-in-high-volatility_1d_oos`
Measure: `measure.py`
