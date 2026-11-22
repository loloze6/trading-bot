---
idea: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: cb945cd336ee
---
Fidelity:
- Situation: a 24-hour fall whose high-low range is a large multiple of its 30-day average 24-hour range -> kept: the component's fall gate is close below its value 6 bars ago, and its range factor is the 6-bar range over the mean 6-bar range across 180 bars.
- Comparison: only while 7-day volatility is high against 60-day volatility, the excess growing with the ratio -> kept: the component multiplies by the 42-bar volatility over its 360-bar mean.
- Outcome: higher than usual return over the next 14 days, larger with the range multiple -> kept: an 84-bar hold, judged against the coin's normal 84-bar drift.
- Verdict transfer: yes: the forecast is the idea's own product of fall gate, range multiple and volatility ratio, and the outcome is its 14-day excess return.
Forecast: The forecast uses FallGatedRangeMultipleVolatilityRatioComponent at period 6, base_period 180, fall_period 6, vol_period 42 and vol_lookback 360. Its value is zero unless the close is below its level 24 hours ago. During such a fall it equals the 24-hour range in multiples of its 30-day mean, times the 7-day volatility over its 60-day mean. It is standardised over its past 402 values. It then goes through signed_power with exponent 3, so ordinary readings are damped towards zero and only large range multiples in turbulent weeks give big positions. The forecast is never negative: long only, and flat when there is no fall.
Config: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: The unusual move per case, measured on the non-overlapping 84-bar grid of each window. A case is a forecast rise of at least 2 points. Each case's 84-bar return from its signal bar has the coin's mean 84-bar return over all windows subtracted. The measure is the mean of these values over all coins, with its ordinary t.
- Supporting check: The mean unusual move of cases in the top half of forecast size, minus that of cases in the bottom half, is greater than 0.
- Confirm: The mean unusual move is greater than 0 with t of 2 or more, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t of -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t with a failed supporting check. Fewer than 30 cases in total is also inconclusive.
