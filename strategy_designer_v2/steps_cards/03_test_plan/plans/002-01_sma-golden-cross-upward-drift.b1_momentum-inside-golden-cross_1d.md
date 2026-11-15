---
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's short moving average of close is above its long one -> kept
- Comparison: the strength of the coin's own rise, or the depth of its drop, over the preceding weeks -> adapted: graded as the 20-bar percent price change, sized continuously rather than by a threshold.
- Outcome: the forward return over the following days is larger after stronger rises, and lower after deeper drops -> kept
- Verdict transfer: yes: the forecast is signed 20-bar momentum, active only while SMA50 is above SMA200, so a slope of forward return on it tests the idea directly.
Forecast: The regime detector marks a bar as trending while SMA(50) is above SMA(200), read from MovingAverageAgeComponent with fast_period 50 and period 200 above 0. On every other bar the forecast is 0. In the trending regime the forecast is the 20-bar percent price change (PriceEvolutionComponent, period 20), standardised against its own 60 past values (min_periods 20, target 10, cap 20). It is long when the coin rose over the last 20 bars and short when it fell. Its size grows with the size of the move, averaging about 10 and capped at ±20.
Config: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The sample is trending-regime bars on the non-overlapping 20-bar grid of each window. For each one, take the next-20-bar return minus the coin's mean 20-bar return over all windows. Regress that excess return on the forecast and report the t of the slope.
- Supporting check: Before costs, the book's mean daily return in the trending regime minus its gain from the market's own rise (the timing part) must be above 0.
- Confirm: The slope's t is 2 or more, on at least 50 independent grid cases, and the timing part is positive.
- Reject: The slope's t is -2 or less, on at least 50 independent grid cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a slope t of 2 or more with a timing part of 0 or less, and so is any result on fewer than 50 grid cases in the trending regime.
