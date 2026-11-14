---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The 50-day vs 200-day simple moving average spread on daily closes: (SMA50 − SMA200) / SMA200 × 100. This is scaled against the mean absolute value of its own previous 200 values, so a typical spread gives about 10, capped at 20. It is then clipped at 0 because the idea is only about upward crosses. The forecast is positive while SMA50 is above SMA200, which is the state that begins at an upward cross. It grows continuously as the short average pulls further above the long one. It is zero while SMA50 is at or below SMA200, and never negative.
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: The horizon is 20 bars. Take one sample at every 20th bar across the six windows and pool them, so returns do not overlap. Measure the close-to-close log return over the next 20 bars. The main measure is the mean of that return on sampled bars where the forecast is above 0, minus the mean over all sampled bars (the random-point and hold baseline), before costs. The idea is confirmed if this excess is above 0 with a t-statistic of at least 2. The supporting check is that the share of positive 20-bar returns on forecast-positive samples is also higher than on all samples.
Reject: The idea is rejected if the excess mean 20-bar return on forecast-positive samples is zero or negative. A clearly negative excess, meaning returns reverse after up-crosses, is a rejection on the brief's own exhaustion clause.
Inconclusive: A positive excess with a t-statistic below 2 neither confirms nor rejects the idea. The same applies if fewer than 8 of the sampled bars have a positive forecast across the six windows, because the forecast was rarely positive.
Deviation: "After an upward cross" becomes "while SMA50 is above SMA200, sized by how far above it is". The position is small right at the cross and largest well after it, when the spread is widest. So the test measures persistence of the up state rather than what follows the cross event itself. Down-crosses from the brief are not traded, because the idea concerns only upward crosses.
