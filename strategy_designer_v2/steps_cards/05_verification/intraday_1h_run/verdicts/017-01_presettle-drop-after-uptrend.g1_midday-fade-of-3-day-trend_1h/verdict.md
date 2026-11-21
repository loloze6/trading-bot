---
plan: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
idea: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean of position x (next 1-bar return - coin mean 1-bar return) on trending bars: 1.8562e-05; ordinary t of the mean: 0.422582 (threshold: confirm: mean > 0 with t >= 2 and >= 4 of 6 coins positive; reject: mean < 0 with t <= -2)
- Supporting check: coins with positive mean excess gain (need >= 4 of 6): 3, passed: False
- Counts: hour-12 cases with a nonzero position: 15082, trending bars in sample: 17347, coins with positive mean excess gain: 3, coins measured: 6
- Decided by: The t of the pooled mean excess gain lies between -2 and 2.
- Reading: Situation bars are those whose next bar starts at 12:00 UTC (bar timestamp 11:00 UTC); the main sample includes every 'trending' bar with a next bar in its window (zero positions included), the coin's mean 1-bar return is over all bars of all its windows, the 500 minimum counts trending bars with a nonzero position, and the coin check needs at least 4 coins with a positive mean whatever the number of coins present.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h`
Measure: `measure.py`
