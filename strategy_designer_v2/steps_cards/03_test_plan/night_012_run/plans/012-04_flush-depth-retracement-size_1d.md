---
idea: 012-04_flush-depth-retracement-size
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: a bar falls sharply on a volume burst with a long lower wick -> kept: a regime rule requires all three on the bar.
- Comparison: a larger open-to-low drop against a smaller one, among those bars -> kept: the position grows with the bar's open-to-low drop.
- Outcome: price rises over the next 3 days, more after a deeper drop -> adapted: the 3-day holding period is dropped, and the 3-bar return is measured from the record.
- Verdict transfer: yes: the criterion reads the 3-bar forward return after every flush bar against the forecast's size, which is exactly the idea's claim.
Forecast: The regime detector marks a flush bar when three conditions hold together. The bar's return is at most -2 usual moves (one-bar return over its 20-bar standard deviation). Its volume is at least 2 times the median of the prior 20 bars. Its lower wick is at least 0.3 of its range. On those bars the forecast is the bar's open-to-low drop in percent, scaled by `standardise` against the mean size of its own last 60 values, with target 5 so that deep drops stay graded below the cap. The forecast is always positive, so it is long only. It is larger the deeper the drop, and zero on every other bar.
Config: 012-04_flush-depth-retracement-size_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: On flush bars (regime mean_reversion, forecast > 0), take the 3-bar forward return close[t+3]/close[t]-1 within the window, minus the coin's mean 3-bar return over all windows. Regress it on the forecast by OLS and take the t of the slope. Cases are counted once: skip any flush bar within 3 bars after a counted one.
- Supporting check: The forecast-weighted mean of the excess 3-bar return over the same cases is above 0.
- Confirm: The slope's t is 2 or more, and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A t of 2 or more with a forecast-weighted mean excess return at or below 0 is also inconclusive. Fewer than 20 independent flush cases across all coins and windows is inconclusive whatever the result.
