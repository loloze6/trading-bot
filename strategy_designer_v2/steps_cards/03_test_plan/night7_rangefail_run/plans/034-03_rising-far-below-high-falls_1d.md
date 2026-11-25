---
idea: 034-03_rising-far-below-high-falls
brief: 034_rising-market-nearness-to-high-drift
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f090b5ff5633
---
Fidelity:
- Situation: the daily close has slipped below its 20-day high, in a rising market -> kept: the close's distance under the highest close of the prior 20 days, clipped to 0 at or above that high, so the book is flat there (the profile is added by code).
- Comparison: the distance is counted in the coin's own daily swings over the last 20 days -> kept: divided by the 20-day standard deviation of daily returns.
- Outcome: the coin falls over the next 5 days, more the more swings below the high -> kept: a graded short held for 5 bars.
- Verdict transfer: yes: the forecast is the idea's own swing-scaled distance below the 20-day high, short only while the close is below it, held for its 5-day horizon.
Forecast: One component, VolatilityScaledDistanceFromHighComponent (period 20, vol_period 20). It gives (close − highest close of the prior 20 days) / that high / the 20-day standard deviation of daily returns. This is negative below the prior high and positive above it. The value is standardised against its own past 60 values (target 10, cap 20), which keeps its sign, and then clipped at a maximum of 0. The forecast is therefore 0 when the close is at or above the 20-day high. Below the high it is negative (a short), and it grows smoothly from 0 in size as the close sits more usual daily swings under the high, up to −20. It is never positive. The code adds the rising profile, so the book is flat outside rising markets.
Config: 034-03_rising-far-below-high-falls_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The excess 5-bar forward return (close[t+5]/close[t] − 1, minus the coin's mean 5-bar return over all its windows) is regressed on the forecast. The sample is bars with a forecast below 0, on the non-overlapping 5-bar grid of each window. The measure is the OLS slope and its t, all coins pooled.
- Supporting check: On the grid bars with a forecast of −10 or below (the deepest slips), the mean excess 5-bar return is below 0.
- Confirm: The slope is positive with t ≥ 2, so deeper below the high means a lower excess return. The supporting check also passes.
- Reject: The slope is negative with t ≤ −2, so deeper below the high means a higher excess return.
- Inconclusive: Anything else is inconclusive. That includes a slope t between −2 and 2, and a slope t ≥ 2 when the deep group's mean excess return is not below 0. At least 100 grid cases with a forecast below 0 are needed, and at least 30 of them at −10 or below; with fewer, the result is inconclusive.
