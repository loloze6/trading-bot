---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Take the gap between the 50-day and the 200-day simple moving averages of the close, (SMA50 − SMA200) / SMA200 × 100. Divide it by the mean absolute value of its previous 200 daily readings and multiply by 10, capping at 20. Then clip it at 0 from below. The forecast is positive while the 50-day average is above the 200-day average, and it grows as the 50-day average pulls further above. It is zero while the 50-day average is at or below the 200-day average, so a cross back down closes the position. It is never negative. The settings are the usual 50/200 daily "golden cross", because the brief gives none.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Confirm: The horizon is 20 bars. Use non-overlapping 20-bar forward close-to-close returns, taken every 20th bar and pooled across the 6 windows. On bars where the forecast is above 0, the mean forward return must beat the mean over all sample bars (the coin held throughout) by at least +1.5 percentage points. This excess must also be positive in at least 4 of the 6 windows. Supporting check: the share of positive forward returns on forecast-above-0 bars beats the share on all bars by at least 5 percentage points.
Reject: The pooled excess 20-bar forward return on forecast-above-0 bars is 0 or below, or it is negative in at least 4 of the 6 windows. Either result means a short average above the long one is followed by no more rise than random points, or by reversal.
Inconclusive: The pooled excess is between 0 and +1.5 percentage points. Or the excess is positive in only 3 of the 6 windows. Or fewer than 8 non-overlapping sample bars carry a forecast above 0.
Deviation: "After the short average crosses above the long one" becomes "while the 50-day SMA is above the 200-day SMA, sized by how far above". The test therefore pools fresh crosses with long-established trends; it is not an event study of the bars just after a cross. The short-side half of the brief and the price-crosses-long-average variant are not tested.
