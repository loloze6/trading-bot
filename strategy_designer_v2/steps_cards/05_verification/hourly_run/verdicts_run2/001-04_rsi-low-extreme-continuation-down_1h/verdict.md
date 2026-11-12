---
plan: 001-04_rsi-low-extreme-continuation-down_1h
idea: 001-04_rsi-low-extreme-continuation-down
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean fwd 24-bar return, most-short forecast decile minus zero-forecast bars: -0.000357322; Newey-West t (24 lags): -0.276843 (threshold: confirm if difference < 0 with Newey-West t <= -2 (24 lags); reject if > 0 with t >= +2)
- Supporting check: slope of demeaned fwd 24-bar return on forecast must be positive: 1.9859e-05, passed: True
- Counts: non-overlapping extreme episodes BTCUSD: 193, non-overlapping extreme episodes ETHUSD: 200, non-overlapping extreme episodes pooled: 393, extreme bars pooled: 9687, zero-forecast bars pooled: 17325, coins with negative difference: 1, coins with positive difference: 1, coins in record: 2
- Decided by: |t| < 2 or the coins split in sign, which the plan calls inconclusive.
- Reading: Most-short decile = bars whose forecast is at or below the 10th percentile of all pooled forecasts (and negative), neutral = forecast exactly 0, Newey-West uses 24 Bartlett lags within each coin-window, per-coin sign uses the plain per-coin mean difference, with only 2 coins present 'at least 2 coins' is applied to those (rejection likewise needs 2 positive coins), and the supporting slope check is reported but not used as a gate since the confirm/reject rules do not name it.
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-04_rsi-low-extreme-continuation-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-04_rsi-low-extreme-continuation-down_1h`
Measure: `measure.py`
