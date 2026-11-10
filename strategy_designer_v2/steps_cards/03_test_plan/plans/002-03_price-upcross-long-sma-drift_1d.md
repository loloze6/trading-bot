---
idea: 002-03_price-upcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The percent distance of the daily close above its 200-day simple moving average, (close − SMA200) / SMA200 × 100. It is standardised against its own past 200 values (window 200, min_periods 50) and clipped at 0, so it is long-only. It is zero whenever the close is at or below the SMA200. It turns positive as soon as the close crosses above the average, and the long position grows with how far the close sits above it. At the past-average distance the forecast is about +10, a 100 % long allocation, capped at +20. It is never negative.
Config: 002-03_price-upcross-long-sma-drift_1d_config.json
Confirm: The test uses a horizon of 20 bars and pools all 6 windows. Sample every 20th bar, so the forward returns do not overlap. Regress the next-20-bar BTC log return in excess of its mean over all bars on the forecast. Confirmation needs a positive slope with t ≥ 2.0. As a supporting check, the portfolio before costs must beat holding BTC at the same average exposure in at least 4 of the 6 windows.
Reject: The idea is rejected if the slope is ≤ 0. It is also rejected if the mean 20-bar forward return on sampled bars with forecast > 0 is below the mean on all sampled bars, which would mean moves above the average reverse. Underperforming exposure-matched holding in 4 or more of the 6 windows would support the rejection.
Inconclusive: A positive slope with t between 0 and 2.0 is inconclusive. So is a set of windows where the forecast is zero, or nearly constant, on almost all bars, giving fewer than about 10 sampled bars with forecast > 0.
Deviation: "After price crosses up through the long average" becomes "while price is above the long average, more the further above". The test does not single out the freshness of the cross: a long-established uptrend counts the same as a new cross. The size is set by the distance from the average, not by the time since the cross. The short-MA-cross variant and the short side of the brief are not tested.
