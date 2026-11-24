---
plan: 031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal_1d
idea: 031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess gain of position x (next-day return - XMR mean daily return): 0.00154697; t of the mean: 4.13712 (threshold: t >= 2 (with the supporting check) confirms, t <= -2 rejects, otherwise inconclusive)
- Supporting check: fall-side slope larger in size than rise-side slope, both negative (|fall| - |rise|): 0.00589645, passed: True
- Counts: bars with a non-zero position: 2887, bars in the main measure: 2897, bars with z < 0: 1355, bars with z > 0: 1539
- Decided by: The mean excess gain has t >= 2 (4.14) and the fall-side reversal slope exceeds the rise-side one, both negative.
- Reading: Every bar with a non-zero volatility-scaled return z (fade_move's raw value) is a bar of the situation, on the side opposite to z's sign; the excess gain is taken on every bar with a next-day return in its window, the coin's mean daily return is the mean of all next-day returns over all windows, the minimum count is of bars with a non-zero postRebalance_current_allocation, and the slopes are ordinary least-squares slopes of next-day return on raw z.
- Size: unusual move +0.51 % (t 4.77, the cases of one day together: 1762 days) per case over 1 bars, 0.110 of the coin's usual move (4.65 %); normal drift in its direction +0.00 %, total +0.52 %; 1762 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal_1d`
Measure: `measure.py`
