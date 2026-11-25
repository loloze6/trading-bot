---
idea: 040-01_rising-swing-scaled-weeks-rise-continues
brief: 040_rising-market-swing-scaled-rise-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: adf647c613f7
---
Fidelity:
- Situation: a coin's 20-day rise in a rising market -> kept: the 20-day return is held only while it is positive, and the code adds the rising profile.
- Comparison: the rise measured against its 20-day daily swings -> kept: the 20-day return divided by the 20-day standard deviation of daily returns, graded by size.
- Outcome: the coin rises more over the next 14 days -> kept: 14 daily bars, long, compared with holding the coin.
- Verdict transfer: yes: the forecast is the idea's swing-scaled rise, and it is held for the idea's 14 days inside the profile the idea names.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 20 and vol_period 20. It is the 20-day return divided by (the 20-day standard deviation of daily returns × √20), which is the rise counted in the coin's own daily swings. The value is standardised over its past 60 values (min_periods 20), then clipped at 0. The forecast is positive and grows linearly with the swing-scaled rise. It is 0 when the 20-day return is zero or negative. It never goes short. The code adds the rising profile, so the book is flat outside rising markets.
Config: 040-01_rising-swing-scaled-weeks-rise-continues_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 14 bars
- Main measure: On each window's non-overlapping 14-bar grid, take every bar in the profile with forecast > 0. Measure the coin's 14-bar forward return minus the coin's mean 14-bar return over all its windows. Find the slope of this excess return on the forecast (least squares), with its t. Group cases by day: a day's deviations are summed.
- Supporting check: The mean excess 14-bar return of all forecast > 0 grid cases is above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes (mean excess return > 0).
- Reject: The slope is negative with t ≤ -2: larger swing-scaled rises are followed by smaller or given-back moves.
- Inconclusive: Any slope with |t| < 2, or a positive slope with t ≥ 2 whose mean excess return is ≤ 0. Fewer than 100 grid cases with forecast > 0, or cases on fewer than 50 distinct days, is inconclusive whatever the t.
