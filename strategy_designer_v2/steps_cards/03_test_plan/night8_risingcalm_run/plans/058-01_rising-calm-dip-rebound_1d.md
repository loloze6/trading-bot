---
idea: 058-01_rising-calm-dip-rebound
brief: 058_rising-calm-pullbacks-recover
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a rising calm market, the 3-day return has fallen below zero -> kept: the profile is added by code, and the forecast is exactly 0 when the 3-day return is at or above zero.
- Comparison: the fall measured against the usual daily swing over the past 30 days -> kept: the 3-day return is divided by the standard deviation of the last 30 daily returns.
- Outcome: the deeper the fall, the larger the rise over the next 5 days -> kept: a long position graded by depth, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's own volatility-scaled pullback, long only and only inside the profile, so a confirm or a reject transfers.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 3 and vol_period 30. This is the 3-day return divided by the 30-day standard deviation of daily returns. Its constant factor sqrt(3) cancels under standardise. The value is standardised over its past 60 values (min_periods 20), then negated, then clipped at 0. The forecast is therefore 0 whenever the 3-day return is at or above zero. When the return is negative, the forecast is positive and grows linearly with the depth of the fall in usual daily swings, up to the cap of 20. It is never negative. Code applies the rising calm profile, so the book is flat outside it.
Config: 058-01_rising-calm-dip-rebound_1d_config.json
Profile: rising calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the non-overlapping 5-bar grid of each window, using the cells with forecast > 0. Take each cell's 5-bar forward return minus the coin's mean 5-bar return over all windows. Regress it on the forecast and measure the slope's t, with cells on the same day pooled.
- Supporting check: The mean of the same excess return over those cells is above 0.
- Confirm: The slope's t is 2 or more, and the mean excess return is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a slope t of 2 or more with a mean excess return at or below 0. At least 30 grid cases with forecast > 0 are needed, else inconclusive.
