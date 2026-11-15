---
idea: 002-03_price-cross-above-long-sma.g1_volatility-scaled-one-day-fall-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's one-day fall, measured in units of its own past 20-day daily volatility -> kept: the 1-bar return over the 20-bar standard deviation of daily returns, counted on falls only (that window includes today's return).
- Comparison: rises above its average return -> kept: the forward return minus the coin's mean return over all windows.
- Outcome: the price rises over the next 1 to 3 days, more after larger falls -> kept: 3-bar forward return, graded by the size of the fall.
- Verdict transfer: yes: the forecast is the fall in volatility units, and its forward excess return is exactly the idea's claim.
Forecast: The indicator is VolatilityScaledReturnComponent with period 1 and vol_period 20. It is today's return divided by the standard deviation of the last 20 daily returns. It is standardised against its own past 60 values, then negated, then clipped at 0, so only falls count. On an up day the forecast is 0. On a down day it is positive, and it grows in proportion to how many usual moves the coin fell: about +10 for an average-sized fall in volatility units, capped at +20. It is never negative, so there is no short after a drop or at any other time.
Config: 002-03_price-cross-above-long-sma.g1_volatility-scaled-one-day-fall-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are bars on the non-overlapping 3-bar grid of each window where the forecast is above 0. For each case, take the forward 3-bar return minus the coin's mean 3-bar return over all windows. Regress that excess return on the forecast and read the slope's t-statistic. This is before costs.
- Supporting check: Take the cases in the top quintile of forecast. Their mean excess 3-bar return, as defined above, must be above 0.
- Confirm: The slope's t is 2 or more, and the top-quintile mean excess return is above 0.
- Reject: The slope's t is -2 or less. Larger falls are then followed by smaller or more negative excess returns.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a t of 2 or more when the top-quintile mean is 0 or below. At least 300 cases with a positive forecast are needed, and at least 60 in the top quintile. With fewer, the result is inconclusive.
