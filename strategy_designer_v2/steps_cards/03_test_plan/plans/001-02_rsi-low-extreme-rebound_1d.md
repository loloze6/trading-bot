---
idea: 001-02_rsi-low-extreme-rebound
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Long only, graded, on every bar. Take the 14-bar Wilder RSI of the daily close. Compute the raw value (50 − RSI) × 0.4, clamped at 0, so it is 0 whenever RSI ≥ 50 and grows linearly as RSI falls below 50. Standardise it by dividing the latest value by the mean absolute value of its previous 60 values, times 10, capped at 20 (window 60, min_periods 20). Then apply signed_power with exponent 2 and pivot 10. Readings below the typical size are damped smoothly towards 0, and deep oversold readings are amplified. The forecast is 0 when RSI ≥ 50, small and positive for a mildly low RSI, and largest (up to the +20 clip, so 200% long) when RSI is at a low extreme relative to its recent past. It is never negative.
Config: 001-02_rsi-low-extreme-rebound_1d_config.json
Confirm: Use a horizon of 5 bars. Pool all coins and windows and take the bars whose forecast is in the top 10% of all tested bars. Count non-overlapping 5-bar forward returns once: after a sampled bar, skip the next 4 bars. For each, compute the forward return minus the same window's mean 5-bar return (the hold-the-coin baseline), before costs. The idea is confirmed if the mean excess return is positive with a t-statistic ≥ 2 and is positive in at least 2 of the 3 coins. Supporting check: the portfolio's return beats holding the coin at the strategy's average allocation.
Reject: The idea is rejected if the mean excess 5-bar return after top-decile forecast bars is ≤ 0 pooled across coins, or if it is negative in at least 2 of the 3 coins, which would mean no rebound or continuation of the decline.
Inconclusive: The result is inconclusive if the pooled mean excess is positive but the t-statistic is below 2, or if it is positive pooled but positive in only 1 coin. It is also inconclusive if fewer than 30 non-overlapping top-decile observations exist.
Deviation: "After RSI reaches a low extreme" becomes "while RSI is below 50, with size growing sharply as it gets more oversold". The position shrinks as RSI recovers towards 50 instead of being held for a fixed number of bars after the extreme. "Extreme" is judged relative to the past 60 bars of the reading, not against a fixed level such as 30.
