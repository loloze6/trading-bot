---
idea: 067-02_choppy-down-stretch-keeps-falling
brief: 067_choppy-average-stretch-carries-forward
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: close below its 20-day average, measured in 20-day standard deviations of daily returns -> kept
- Comparison: the stretch is judged against the coin's own 20-day daily swing -> kept
- Outcome: the coin falls over the next 10 days, more so the larger the stretch -> kept
- Verdict transfer: yes: the forecast is exactly the idea's stretch below the average, and it is held for the idea's 10 days.
Forecast: The forecast uses one indicator, MovingAverageDistanceComponent with period 20, SMA and base "usual_moves" (vol_period 20). It reads the close's distance from its 20-day SMA, counted in 20-day standard deviations of daily returns. The distance is standardised over its past 60 values (min_periods 20), then clipped at a maximum of 0. The forecast is therefore 0 when the close is at or above the average. Below the average it is negative (short), and its size grows linearly with how far the close sits below the average in usual moves, up to the cap of -20. It is never positive. The choppy profile is added by code, so the book is flat outside choppy markets.
Config: 067-02_choppy-down-stretch-keeps-falling_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window, on bars with forecast < 0. Regress the coin's 10-bar forward return minus its normal drift (its mean 10-bar return over all windows) on the forecast's size (-forecast), and read the slope's t. Report the number of independent cases next to the t.
- Supporting check: On the same cases, the mean unusual move in the short direction (minus the 10-bar return net of drift) must be above 0.
- Confirm: The slope is negative with t ≤ -2: a larger stretch below the average is followed by a larger fall net of drift. The supporting check must also pass.
- Reject: The slope is positive with t ≥ +2: a larger stretch below the average is followed by a larger rise toward the average, which is reversion.
- Inconclusive: Any slope t between -2 and +2 is inconclusive. A confirming slope with a failed supporting check is also inconclusive. So is any result from fewer than 30 grid cases with forecast < 0, across all coins and windows.
