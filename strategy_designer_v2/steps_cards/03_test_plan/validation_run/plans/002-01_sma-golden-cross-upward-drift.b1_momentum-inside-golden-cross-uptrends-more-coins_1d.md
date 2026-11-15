---
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the 50-day SMA is above the 200-day SMA, with the coin's own 20-day return as the signal -> kept: a regime rule on SMA50 above SMA200, and the 20-day return measured as stated.
- Comparison: a higher 20-day return against a lower one -> kept: the forecast grows with the 20-day return.
- Outcome: a larger return over the next 10 days -> kept: horizon of 10 bars.
- Verdict transfer: yes: the test measures exactly whether the 10-day return rises with 20-day momentum while SMA50 is above SMA200.
Forecast: Each bar is classed `trending` while the 50-bar SMA is above the 200-bar SMA (an SMA-pair spread above 0). On every other bar the forecast is 0. On `trending` bars the forecast is the 20-bar percent return, standardised against its 60 past values (target 10, cap 20). It is positive and grows with a stronger 20-day rise. It is negative and grows with a deeper 20-day fall, which is the "refuse longs" side. It is near 0 when the 20-day return is flat.
Config: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Take the non-overlapping grid bars (positions 0, 10, 20, ... of each window) where the regime is `trending`. On those bars, regress each coin's 10-bar forward return, minus that coin's mean 10-bar return over all windows, on the forecast. Read the slope's t.
- Supporting check: On the same cases, the mean excess 10-bar return of the top third of forecasts, minus that of the bottom third, is above 0.
- Confirm: The slope is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The slope is below 0 with t ≤ -2.
- Inconclusive: A t between -2 and 2 is inconclusive, and so is a confirming slope whose supporting check fails. The test needs at least 100 independent trending cases; with fewer, the result is inconclusive.
