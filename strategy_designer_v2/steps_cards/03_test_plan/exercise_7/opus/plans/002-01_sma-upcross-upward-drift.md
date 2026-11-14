---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The forecast is the percent spread between the 50-day and 200-day simple moving averages of the close: (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own last 200 daily values, so an average-sized spread is about 10 and the cap is 20. It is then clipped below at 0. The forecast is positive and grows with the spread while the 50-day average is above the 200-day average. It is 0 when the 50-day average is at or below the 200-day average. It is never negative, because the idea is only about upward crosses. The forecast starts from 0 at the moment of the cross and grows as the short average pulls away from the long one, so the position is built up gradually rather than switched on.
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: The test uses a horizon of 20 bars and samples every 20th bar, so the forward returns do not overlap (about 36 samples across the 6 windows). The forward return is demeaned by the mean 20-bar return of its own window, so the coin's own rise is not credited to the idea. The idea is confirmed if two things hold. First, the slope of the demeaned forward 20-bar log return on the forecast at the start of each sample is positive with t ≥ 2. Second, as a supporting check, the samples with forecast > 0 have a demeaned mean forward return above 0 in at least 4 of the windows that contain such samples.
Reject: The idea is rejected if the slope is ≤ 0. It is also rejected if the samples with forecast > 0 show a demeaned mean forward return below 0 with t ≤ −1, which would mean moves after upward crosses fade or reverse relative to random points.
Inconclusive: The test is inconclusive if the slope is positive with t below 2. It is also inconclusive if fewer than 10 non-overlapping samples have a forecast above 0, for example because the 50-day average stays below the 200-day average through most windows.
Deviation: "After an upward cross" becomes "while the 50-day SMA is above the 200-day SMA, sized by how far apart they are." The forecast does not single out the bars just after the cross: it is small there and largest when the trend is well established. So it tests persistence of the whole above-the-long-average state, not the freshness of the cross. The cross of price itself over the long average and the downward cross from the brief are not tested.
