---
plan: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar excess return of the bets over the coin's normal drift: 0.00178264; ordinary t of the mean: 1.12554 (threshold: t >= 2 over at least 100 cases confirms; t <= -2 over at least 100 cases rejects)
- Supporting check: Welch t of high-forecast half minus low-forecast half mean excess return: None, passed: None
- Counts: cases: 3102, high-forecast half: 0, low-forecast half: 3102
- Decided by: The mean excess return's t is between -2 and 2 over at least 100 cases.
- Reading: A bet is a rise of the positive forecast of at least 2 points from its lowest level since the last bet (from 0 after a flat bar), the first bet in each 18-bar grid cell (positions 0,18,... of the window) is the case, the drift is the coin's mean non-overlapping 18-bar return over all windows, the high half is the cases with entry forecast strictly above the median, and fewer than 100 cases is reported as not observable; the situation is the close above the prior 12-bar high (from the component's raw value > 0 on a window's first 12 bars).
- Size: unusual move +0.18 % per case over 18 bars, 0.020 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.58 %; 3102 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h`
Measure: `measure.py`
