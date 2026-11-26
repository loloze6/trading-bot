---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a heavy-volume day against its own prior 20-day average, closing low in its range -> adapted: "heavy" is a regime (volume at least 1.5 times its prior 20-day mean, the common convention), and inside it the size grows with the volume ratio times the close's nearness to the low.
- Comparison: the day's volume against its own prior 20-day average -> kept
- Outcome: the coin rises over the next day, more the heavier the volume and the lower the close -> kept: long only over 1 bar, flat when the close sits at the high.
- Verdict transfer: yes: the forecast is the idea's product of the volume surge and the close's depth in the range, and it is held over the idea's one-day horizon, so its result is the idea's result.
Forecast: The forecast is non-zero only on days whose volume is at least 1.5 times the mean of the prior 20 days' volume. On those days it is long and sized by (high − close) / (high − low) × volume / mean of the prior 20 days' volume. That value is standardised over its last 60 values (min 20). It is 0 with the close at the high and grows as the close nears the low and as the surge grows. It is never negative. On every other day it is 0.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On heavy-volume (regime "trending") days, the next-day return minus the coin's mean daily return over all windows is regressed on the forecast. The measure is the t of the slope, with cases of the same day pooled across coins.
- Supporting check: On the same days, the mean excess next-day return of the top-third forecasts minus that of the bottom-third forecasts (Welch) is above 0.
- Confirm: The slope t is 2 or more and the top-minus-bottom difference is above 0.
- Reject: The slope t is −2 or less.
- Inconclusive: A slope t between −2 and 2, or a t of 2 or more with a top-minus-bottom difference of 0 or less, neither confirms nor rejects. Fewer than 100 heavy-volume days spread over at least 50 distinct dates is also inconclusive.
