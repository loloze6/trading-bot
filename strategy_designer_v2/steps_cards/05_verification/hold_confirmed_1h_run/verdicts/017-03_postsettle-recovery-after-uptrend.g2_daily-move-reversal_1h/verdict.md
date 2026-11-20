---
plan: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h
idea: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (next-24-bar return minus coin's mean 24-bar return), non-overlapping: 0.00170974; ordinary t of the mean: 3.80116 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 500 non-overlapping cases)
- Supporting check: mean product, top third |forecast| minus bottom third: 0.00375391, passed: True
- Counts: non-overlapping cases: 17246, active bars: 416370
- Decided by: The mean is positive with t >= 2, and the largest-|forecast| third beats the smallest third.
- Reading: The coin's mean 24-bar return is taken over its non-overlapping grid samples in all windows; the thirds are the floor(n/3) cases with the largest and smallest |forecast| (stable sort); fewer than 500 cases is reported as 'not observable' as instructed; the situation side uses the in-window price 24-bar return, and the raw component value where the window has fewer than 24 prior bars.
- Size: unusual move +0.12 % per case over 24 bars, 0.023 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total +0.11 %; 17056 cases
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h`
Measure: `measure.py`
