---
idea: 003-03_heavy-volume-rise-continues
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a sharp one-day rise on volume well above its own 30-day average -> adapted: the "sharp" and "well above" thresholds become graded, as the day's rise in usual moves times its volume ratio.
- Comparison: volume against the coin's own 30-day average daily volume -> kept
- Outcome: the price keeps rising over the next 5 days, more after larger and heavier rises -> adapted: the 5-day hold is dropped, so the position is held only while the rise bar is current and the 5-bar forward return is measured.
- Verdict transfer: yes: the test grades rises by size and relative volume and checks for a continued 5-day gain above holding, so a confirm or a reject carries over to the idea.
Forecast: One indicator, VolumeWeightedScaledReturnComponent (vol_period 20, volume_period 30). It is today's one-day return divided by the 20-day standard deviation of daily returns, times today's volume over its 30-day mean volume. It is standardised against its own past 60 values (min_periods 20) and clipped at 0, so falls and flat days give 0 and the forecast never goes short. A cubic graded dead zone (signed_power, exponent 3, pivot 20) then keeps ordinary up days near 0. The forecast is positive only after up days. It grows with the cube of the rise times its relative volume, reaching about +20 for the largest heavy-volume rises.
Config: 003-03_heavy-volume-rise-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window (positions 0, 5, 10, ...). On grid bars with forecast >= 2, take the excess return: close[t+5]/close[t] - 1 minus that coin's mean 5-bar return over all its windows together. The measure is the mean of this excess return, with the ordinary t of the mean.
- Supporting check: Over the same signal bars, the Spearman correlation between the forecast and the excess return is above 0. This checks that larger and heavier rises are followed by larger gains.
- Confirm: The mean excess return is above 0 with t >= 2, and the Spearman correlation is above 0.
- Reject: The mean excess return is below 0 with t <= -2, meaning heavy-volume rises are followed by underperformance against holding.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 with a Spearman correlation of 0 or below is also inconclusive. At least 30 signal grid bars across all coins and windows are needed; with fewer the result is inconclusive.
