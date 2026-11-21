---
plan: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud_1d
idea: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean drift-adjusted 26-bar short gain: 0.02771; t of the weighted mean: 1.15284 (threshold: confirm: mean > 0 with t >= 2 on >= 30 cases and check passes; reject: mean < 0 with t <= -2 on >= 30 cases)
- Supporting check: mean drift-adjusted return, larger minus smaller |forecast| half (< 0): -0.0795721, passed: True
- Counts: cases: 156, active bars: 4916, larger half: 78, smaller half: 78
- Decided by: The t of the weighted mean short gain lies between -2 and 2 on at least 30 cases.
- Reading: Situation = close below the lower edge of the 9/26/52/26 cloud (recomputed from the window's prices, the detector's 'trending' regime where too few bars exist) and the cloud_fall raw slope < 0, side short; drift = each coin's mean non-overlapping 26-bar return over all its windows; the t of the weighted mean uses the weighted standard error sqrt(sum w^2 (x-m)^2)/sum w; the larger half is |forecast| above the median, the smaller half at or below it.
- Size: unusual move +2.33 % per case over 26 bars, 0.108 of the coin's usual move (25.48 %); normal drift in its direction -4.06 %, total -1.73 %; 209 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud_1d`
Measure: `measure.py`
