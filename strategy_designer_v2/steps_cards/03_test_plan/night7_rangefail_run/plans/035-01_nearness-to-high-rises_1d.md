---
idea: 035-01_nearness-to-high-rises
brief: 035_nearness-to-high-drift-any-market
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f090b5ff5633
---
Fidelity:
- Situation: a daily close's distance below its 20-day high, counted in daily swings -> kept: the distance of the close from the prior 20-day closing high, divided by the 20-day standard deviation of daily returns.
- Comparison: fewer swings below the high against more -> kept: a graded relation, positive when nearer the high than the coin's usual distance and negative when farther.
- Outcome: the coin rises more over the next 5 days -> kept: the 5-bar forward return, beyond the coin's normal drift, grows with the forecast.
- Verdict transfer: yes: a positive slope of the 5-day excess return on the nearness forecast is the idea, and a reversed slope rejects it.
Forecast: VolatilityScaledDistanceFromHighComponent (period 20, vol_period 20) gives (close − prior 20-day highest close) / that high / 20-day std of daily returns. It is negative below the high, 0 at it and positive above it. Standardise uses window 60 and min_periods 20, so x averages about −10. It is averaged at equal weight with the standardised constant +10, so the forecast is (x + 10) / 2. The forecast is positive and grows when the close sits fewer swings below its high than usual, or stands above it (up to about +15). It is near 0 at the usual distance. It is negative, down to about −5, when the close sits deeper than usual. The forecast is graded throughout, ungated and applies in every market.
Config: 035-01_nearness-to-high-rises_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use non-overlapping 5-bar grid cells (positions 0, 5, 10, ... of each window). For each cell, take the coin's 5-bar forward return minus that coin's mean 5-bar return over all its windows (normal drift). Regress this excess return on the recorded forecast at the cell's bar, pooled over coins and windows. Report the slope's t, with cases of the same day taken together.
- Supporting check: The same slope, computed only on cells where the coin's 60-day return (recomputed from closes inside the window) is at or below +10 %, has a positive estimate.
- Confirm: The main slope has t ≥ 2, and the supporting check's slope is above 0.
- Reject: The main slope has t ≤ −2.
- Inconclusive: A main slope with t between −2 and 2 is inconclusive. So is a t ≥ 2 whose non-rising-market slope is at or below 0. The test needs at least 500 grid cases over at least 100 distinct days; with fewer it is inconclusive.
