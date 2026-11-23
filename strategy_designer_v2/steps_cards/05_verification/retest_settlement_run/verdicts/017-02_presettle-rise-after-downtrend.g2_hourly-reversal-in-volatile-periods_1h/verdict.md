---
plan: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of next-hour excess return on fade_1h forecast: 2.13161e-05; OLS slope t: 13.7732 (threshold: t >= 2 with supporting check passing confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: slope on high-vol bars minus slope on low-vol bars: 2.6618e-05, passed: True
- Counts: bars in total: 416645, bars with high 24h volatility: 119877, bars with low 24h volatility: 189776
- Decided by: The slope's t is 2 or more and the high-vol slope exceeds the low-vol slope.
- Reading: The situation is any bar with a non-zero last-hour move (raw fade_1h value, or the close-to-close return where it is missing) and the expected side is opposite to that move; the regression uses every bar with a recorded post_pipeline_value and a next-hour return inside its window (zero forecasts included), and the volatility groups use the 24-bar standard deviation of hourly returns against its full 720-bar rolling mean computed inside each window, bars without that mean left out of the groups.
- Size: unusual move +0.01 % per case over 1 bars, 0.013 of the coin's usual move (1.05 %); normal drift in its direction -0.00 %, total +0.01 %; 263630 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h`
Measure: `measure.py`
