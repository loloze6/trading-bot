---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: Long only, graded by the spread between the 50-bar and 200-bar simple moving averages of the close, on 1h bars (the conventional "golden cross" pair; the brief gives no lengths). The raw value is (SMA50 − SMA200) / SMA200 × 100. It is standardised against the mean absolute value of its own previous 200 values (target 10, cap 20), then clipped at 0. The forecast is positive exactly while SMA50 is above SMA200, which is the stretch from an upward cross to the next downward cross. It grows with how far the short average sits above the long one, up to +20. It is 0 from the downward cross until the next upward cross. It is never negative.
Config: 002-05_sma-up-regime-positive-drift_1h_config.json
Confirm: Horizon is 24 bars. In each window, take every 24th bar and its forward 24-bar log return of the close, so the returns do not overlap. The main measure is the mean forward return on sampled bars where the forecast is above 0 minus the mean forward return on all sampled bars, before costs. The idea is confirmed if this difference, pooled over the 6 windows, is positive with a t-statistic of at least 2 and is positive in at least 4 of the 6 windows. The supporting check must also hold: the share of positive forward returns is higher on in-stretch bars than on all sampled bars.
Reject: The idea is rejected if the pooled difference is zero or below. A difference that is negative with a t-statistic of −2 or lower also rejects it, more strongly: moves after an upward cross reverse rather than persist.
Inconclusive: The result is inconclusive if the pooled difference is positive but its t-statistic is below 2. It is also inconclusive if the difference is positive overall but positive in fewer than 4 of the 6 windows.
Deviation: The idea gives equal weight to every bar of the stretch from an upward cross to the next downward cross. The config holds a position on exactly those bars, but sizes it by the width of the SMA50–SMA200 spread rather than holding a fixed amount. The criterion, however, uses only the in-stretch versus all-bars split (forecast > 0), so the sizing does not enter the verdict. The 50/200 lengths are a convention, not taken from the source script. The short side and the brief's "price crosses the long average" variant are not tested.
