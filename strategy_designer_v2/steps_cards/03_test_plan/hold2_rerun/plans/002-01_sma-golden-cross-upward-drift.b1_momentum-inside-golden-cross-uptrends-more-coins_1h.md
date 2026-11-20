---
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin's 50-day SMA is above its 200-day SMA -> kept: a regime rule on the 1200-bar against the 4800-bar SMA.
- Comparison: the higher the coin's own 20-day return -> kept: the 480-bar return, graded, flat when it is negative as the consequence says.
- Outcome: a larger return over the next 10 days -> kept: the 240-bar forward return, judged against the coin's mean.
- Verdict transfer: yes: the test measures the same condition, signal and horizon the idea states.
Forecast: The regime is `trending` while the 1200-bar SMA (50 days) is above the 4800-bar SMA (200 days); every other bar is flat. In that regime the forecast is the coin's 480-bar (20-day) percent return, divided by the mean absolute size of its previous 480 values times 10, and capped at ±20. Negative values are clipped to 0, so in an uptrend whose last 20 days fell the forecast is 0. The forecast is positive and grows with the 20-day rise, never short.
Config: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h_config.json
Criterion:
- Horizon: 240 bars
- Main measure: Use the bars whose regime is `trending`, taken on each window's non-overlapping 240-bar grid. On those bars, regress the next 240-bar return, minus the coin's mean 240-bar return over all windows, on the forecast at t (zeros included). Report the slope's t across all coins and windows pooled.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2. Excess forward return rises with the size of the 20-day-momentum position.
- Reject: The slope is negative with t ≤ -2. Higher 20-day momentum inside uptrends is followed by smaller excess returns.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive, as is a run with fewer than 200 grid cases in `trending`. It is also inconclusive with fewer than 50 cases at forecast 0 or fewer than 50 with forecast > 0.
