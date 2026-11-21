---
idea: 022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 1-day rise relative to its daily volatility over the past 30 days -> kept
- Comparison: the coin's normal drift -> kept
- Outcome: the coin rises above its normal drift over the next 5 days, more after a larger scaled rise -> kept
- Verdict transfer: yes: the forecast is the 1-day rise in 30-day volatility units, held 5 days and judged against the coin's drift, which is exactly the idea's claim.
Forecast: The forecast starts from VolatilityScaledReturnComponent with period 1 and vol_period 30. Its raw value is today's 1-day return divided by the standard deviation of the last 30 daily returns. This value is standardised over the 60 prior values (min_periods 20), so a usual-sized move reads about 10, capped at 20. It is then clipped at 0, so the forecast is never short. The forecast is positive after an up day and grows with the size of the rise in usual moves. It is zero on down or flat days, and it is never negative.
Config: 022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The grid is non-overlapping 5-bar points in each window. On the grid bars with forecast > 0, regress the coin's 5-bar return from that close, minus its normal drift, on the forecast. The normal drift is the coin's mean 5-bar return over all windows. The measure is the OLS slope's t.
- Supporting check: The forecast-weighted mean of that 5-bar excess return over the same cases is above 0.
- Confirm: The slope's t is 2 or more, and the forecast-weighted mean excess return is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A t of 2 or more with a forecast-weighted mean excess return at or below 0 is also inconclusive. Fewer than 300 positive-forecast grid cases, pooled over coins and windows, is inconclusive whatever the t.
