---
plan: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d
idea: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 26-bar return in excess of the coin's drift: 0.015116; ordinary t of the mean: 0.689244 (threshold: confirm if t >= 2 with >= 30 cases and Spearman > 0; reject if t <= -2 with >= 30 cases)
- Supporting check: Spearman of |forecast| vs short-direction excess return: 0.141119, passed: True
- Counts: non-overlapping cases: 156
- Decided by: Main t lies between -2 and 2 (inconclusive rule).
- Reading: Situation recomputed from each window's own prices (Ichimoku 9/26/52, cloud at t = spans computed at t-26, close below the lower span and cloud mid lower than 26 bars before), agreement taken over active bars where it is computable; the plan's 'fewer than 30 cases' is treated as its minimum count, giving 'not observable'.
- Size: unusual move +2.79 % per case over 26 bars, 0.113 of the coin's usual move (25.48 %); normal drift in its direction -4.15 %, total -1.36 %; 241 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d`
Measure: `measure.py`
