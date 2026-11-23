---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 91c94c46188e
---
Fidelity:
- Situation: a down day closing near its low, on heavy volume -> adapted: the down day is a regime (close below the prior close), and "heavy" is graded through the volume ratio times the close's nearness to the low.
- Comparison: volume against its prior 20-day average -> kept: today's volume over the mean of the prior 20 days, with today left out.
- Outcome: the coin rises over the next day, more after heavier volume -> kept: the next 1-day return, long, sized by the product.
- Verdict transfer: yes: the forecast is the idea's own product of close location and volume ratio on down days, judged on the next day's move.
Forecast: Only on down days (today's close below yesterday's close), the forecast is the share of the day's range between the close and the high, multiplied by today's volume over the mean of the prior 20 days' volume (VolumeWeightedCloseLocationComponent, volume_period 20, exclude_current 1, reference "high"). It is standardised against its last 60 values, then passed through signed_power with exponent 2 and pivot 10, so that light-volume or mid-range closes give a small position and heavy-volume closes at the low give a large one. The forecast is never negative, so the book is long or flat. It is 0 on up and flat days. It grows when the close sits nearer the low and when the volume is heavier.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next day's return on the forecast, across every down-day bar with a forecast above 0 (1-bar grid, inside windows). The return is the next day's coin return minus that coin's mean daily return over all its windows. The measure is the t of that slope.
- Supporting check: The top fifth of down-day bars by forecast must have a mean next-day excess return above 0.
- Confirm: The slope's t is 2 or more and the top-fifth mean excess return is above 0. Both are before costs.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with the top-fifth mean at or below 0. At least 200 down-day bars with a forecast above 0 are needed, across all coins and windows; with fewer, the test is inconclusive.
