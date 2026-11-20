---
plan: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess next-bar return on forecast > 0 bars: 0.00996434; ordinary t of forecast/10 x excess return: 4.9472 (threshold: weighted mean > 0 with ordinary t of (forecast/10 x excess) >= 2 to confirm; t <= -2 to reject)
- Supporting check: mean excess next-bar return, high-volume-ratio half minus low half (Welch t): 0.0091524, passed: True
- Counts: active bars: 1514, high volume half: 757, low volume half: 757
- Decided by: Weighted mean excess return > 0 with t >= 2 and the high-volume half beats the low half (confirm rule).
- Reading: Volume halves split active bars sorted by the recorded vol.last_history_value into the lower n//2 and upper n//2 (middle bar dropped when n is odd); the supporting check passes when high minus low > 0; the plan's 'fewer is inconclusive' minimum is reported as 'not observable' per the workflow; the situation check uses recorded component values where present and recomputes them from prices otherwise.
- Size: unusual move +0.78 % per case over 1 bars, 0.163 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.90 %; 1023 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d`
Measure: `measure.py`
