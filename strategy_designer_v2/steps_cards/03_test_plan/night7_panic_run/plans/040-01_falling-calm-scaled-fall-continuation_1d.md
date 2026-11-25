---
idea: 040-01_falling-calm-scaled-fall-continuation
brief: 040_calm-downtrend-falls-keep-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in a falling, calm market, a coin that has fallen over the last 3 days -> kept: the falling calm profile is added by code, and the 3-day fall is kept by clipping the forecast to the fall side only.
- Comparison: the 3-day fall measured in units of the coin's 30-day daily-return swing -> kept: the 3-day return is divided by the standard deviation of the last 30 daily returns, and the forecast is graded by that size.
- Outcome: the coin keeps declining over the next 3 days, more so the larger the scaled fall -> kept: a short position sized by the scaled fall, held for 3 bars.
- Verdict transfer: yes: the book is short only after 3-day falls inside falling calm markets, and it is sized by the scaled fall, so both of the brief's failure conditions can show.
Forecast: One `VolatilityScaledReturnComponent` with `period` 3, `vol_period` 30 and `lag` 0. It gives the 3-day return divided by (the 30-day standard deviation of daily returns x sqrt 3); the constant sqrt 3 cancels in `standardise`. It is standardised over 60 bars (min_periods 20), then clipped at a maximum of 0. The forecast is negative (short) only after a 3-day fall, with a size that grows linearly with the fall in usual daily moves, about -10 for a typical size and capped at -20. It is 0 after a 3-day rise or a flat 3 days. The code keeps it at 0 outside falling calm markets.
Config: 040-01_falling-calm-scaled-fall-continuation_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the bars at positions 0, 3, 6, ... of each window where the forecast is below 0. For each case, take the coin's 3-bar return from that close minus the coin's mean 3-bar return over all its windows (non-overlapping), with the sign flipped so a further fall is positive. Measure the mean of this value and its t, with cases on the same day summed together.
- Supporting check: Over the same cases, the least-squares slope of the drift-removed 3-bar return on the forecast. It must be positive: a more negative forecast is followed by a more negative return. Its t is computed with the same day clustering.
- Confirm: The main measure's mean is above 0 with t >= 2, and the supporting slope is above 0 with t >= 2.
- Reject: The main measure's t <= -2 (a rebound beyond drift), or the supporting slope's t <= -2 (larger scaled falls are followed by less decline).
- Inconclusive: Any other result, including t between -2 and 2 on either measure. It is also inconclusive with fewer than 30 cases, or with cases on fewer than 30 distinct days.
