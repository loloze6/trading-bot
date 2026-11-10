---
idea: 002-06_sma-down-regime-negative-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The 50-day simple moving average minus the 200-day simple moving average, as a percent of the 200-day average. The 50/200 setting is the most common convention for a daily SMA cross. The forecast is standardised against its own last 200 values and then cut at zero from above, so it is short only. It is negative while the 50-day SMA is below the 200-day SMA, which is the stretch from a downward cross to the next upward cross. Its size grows with how far the short average sits below the long one. It is zero on every bar where the short average is at or above the long one.
Config: 002-06_sma-down-regime-negative-drift_1d_config.json
Confirm: The horizon is 1 bar: the close-to-close return of the bar after each forecast. Pool all six windows. Take the 1-bar returns on bars where the forecast is negative and subtract the mean 1-bar return of all bars, which is the coin simply held. This difference must be below zero with a t-statistic of -2 or lower, measured before costs. Supporting check: on the strategy's short bars, the portfolio's value must rise in total, and the share of those bars that close lower must be above 50%.
Reject: The idea is rejected if the mean 1-bar return on negative-forecast bars is at or above the all-bar mean. It is also rejected if the short positions lose in total before costs, which would mean prices after the downward cross reverse or drift like random stretches.
Inconclusive: The test is inconclusive if fewer than 30 negative-forecast bars exist across all windows. It is also inconclusive if the difference is negative but its t-statistic lies between -2 and 0.
Deviation: The idea treats every bar of the stretch alike, from the downward cross until the next upward cross. The config instead sizes the short by how far the 50-day SMA sits below the 200-day SMA, so bars just after the cross carry a small position. The long side after an upward cross is left out, because this idea concerns only the downward stretch.
