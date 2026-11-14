---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The 50-day simple moving average minus the 200-day simple moving average, as a percent of the 200-day average. Each bar's value is divided by the mean absolute value of the 200 values before it, times 10 and capped at ±20, then clipped at 0 below. The forecast is positive while the 50-day SMA is above the 200-day SMA, which is the stretch after an upward cross. It is zero while the 50-day SMA is below, which is the stretch after a downward cross. It grows continuously as the 50-day average pulls further above the 200-day average. It is never negative.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Confirm: Horizon is 1 bar (the next day's close-to-close BTC return), so no returns overlap. Pool all 6 windows. The idea is confirmed if two things hold. First, the mean next-bar return on bars with forecast > 0 exceeds the mean next-bar return on all bars by an amount with t-stat ≥ 2. Second, as the supporting check, the share of up days on forecast > 0 bars is higher than the share on all bars.
Reject: The idea is rejected if the pooled mean next-bar return on forecast > 0 bars is at or below the mean over all bars. This applies when both the forecast > 0 bars and the forecast = 0 bars number at least 60. That result means that being in an up-cross stretch adds nothing over holding the coin, or that the stretch is followed by reversal.
Inconclusive: The test is inconclusive in two cases. One is a positive difference with t-stat below 2. The other is fewer than 60 pooled bars in either state (forecast > 0 or forecast = 0), since crosses of the 50/200 averages are rare in 6 windows of about 122 days.
Deviation: The idea is a binary state: in an up-cross stretch or not. The config tests it as a position that is sized by how far the 50-day SMA sits above the 200-day SMA. The criterion judges only the state (forecast > 0 versus all bars), not the size. The idea names no averages, so the conventional daily 50/200 SMA pair stands in for "short" and "long". Down-cross stretches are held flat, not short, because the idea speaks only of the upward stretch.
