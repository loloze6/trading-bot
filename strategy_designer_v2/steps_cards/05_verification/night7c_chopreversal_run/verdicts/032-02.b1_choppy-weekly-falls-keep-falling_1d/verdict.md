---
plan: 032-02.b1_choppy-weekly-falls-keep-falling_1d
idea: 032-02.b1_choppy-weekly-falls-keep-falling
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move of short cases (short direction): 0.0106427; day-clustered t: 1.41138 (threshold: mean > 0 with t >= 2 (and supporting check) confirms; mean < 0 with t <= -2 rejects)
- Supporting check: stronger minus weaker (above vs at/below median forecast size) mean unusual move: -0.00559688, passed: False
- Counts: cases: 441, distinct days: 350
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation = 7-bar close return < 0 (from prices) and chop.last_history_value < 0.3 (prices if missing) and the volatility-percentile condition read from regime == mean_reversion (it cannot be rebuilt from a window's prices), short side expected; cases = first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet) per 7-bar grid cell of each window, drift = coin's mean non-overlapping 7-bar grid return over all its windows, day-clustered t with G/(G-1) correction, forecast size = |forecast| at the signal bar.
- Size: unusual move +1.06 % (t 1.41, the cases of one day together: 350 days) per case over 7 bars, 0.075 of the coin's usual move (12.44 %); normal drift in its direction -0.89 %, total +0.17 %; 441 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-02.b1_choppy-weekly-falls-keep-falling_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-02.b1_choppy-weekly-falls-keep-falling_1d`
Measure: `measure.py`
