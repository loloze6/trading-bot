---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Ungated and long only. Compute the spread between the 20-day and the 50-day simple moving average of the close: (SMA20 − SMA50) / SMA50 × 100. Standardise it against its own past 60 daily values, with min_periods 20: the latest spread divided by the mean absolute spread of the 60 bars before it, times 10, capped at ±20. Then clip it at 0. - The forecast is positive while SMA20 is above SMA50. - It grows with how far the short average has pulled above the long one: about +10 for a typical gap, up to +20. - It is zero while SMA20 is at or below SMA50, so a downward cross closes the position. - It is never negative.
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: The main measure uses a horizon of 10 bars. On every 10th bar of each window (non-overlapping), take BTC's forward 10-bar close-to-close return. Average it over the bars where the forecast is above 0, and subtract the average over all sampled bars of the same window. - The idea is confirmed if this excess is positive in at least 4 of the windows that have active bars (at least 3 such windows are needed), and the pooled excess has t ≥ 2. - Supporting check: the strategy's return minus (its average allocation × the buy-and-hold return of the window) is positive when pooled over the windows.
Reject: The idea is rejected if the pooled excess forward 10-bar return on active bars is ≤ 0. It is rejected outright, as moves that reverse after the cross, if that excess is negative with t ≤ −2.
Inconclusive: Any of these neither confirms nor rejects the idea: - the pooled excess is positive but t < 2; - the excess is positive in fewer than 4 of the active windows; - fewer than 3 windows have any bar with a forecast above 0.
Deviation: The idea says "after an upward cross"; the config tests "while SMA20 is above SMA50", sized by the gap between them. So the largest positions come well after the cross, once the averages have spread apart, not at the cross itself. The 20/50 periods are a convention I chose, because the source gives no lengths.
