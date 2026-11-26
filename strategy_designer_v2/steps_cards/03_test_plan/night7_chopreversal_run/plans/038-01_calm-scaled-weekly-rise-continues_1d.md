---
idea: 038-01_calm-scaled-weekly-rise-continues
brief: 038_calm-market-scaled-move-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in a calm market, a coin's 7-day rise -> kept: the 7-day return, positive part only, with calm applied as the brief's profile
- Comparison: the rise measured against its 30-day daily swing -> kept: the 7-day return divided by the 30-day standard deviation of daily returns
- Outcome: a larger further rise over the next 5 days, growing with the scaled rise -> kept: the long position grows with the scaled rise and is held 5 bars
- Verdict transfer: yes: the forecast is exactly the scaled 7-day rise inside calm bars, so its 5-day gains confirm or reject the idea directly.
Forecast: The forecast uses one component, VolatilityScaledReturnComponent with period 7, vol_period 30, lag 0 and vol_lookback 1. It is the 7-day return divided by (the 30-day daily return standard deviation x sqrt 7). The constant sqrt 7 cancels under standardisation. The value is standardised against its own 60 past values (min_periods 20), which gives an average size of about 10, capped at 20. It is then clipped at 0, so it is long only. The forecast is 0 when the coin did not rise over the 7 days. It grows linearly with the size of the rise in usual swings. Code adds the calm profile, so the book is flat on agitated bars.
Config: 038-01_calm-scaled-weekly-rise-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the non-overlapping 5-bar grid of each window, using bars with forecast > 0. On it, regress the coin's 5-day forward return minus its normal 5-day drift (the mean over all windows) on the forecast. The measure is the slope's t, with the number of cases reported.
- Supporting check: The mean unusual 5-day move over the same cases is above 0, before costs and net of the coin's drift.
- Confirm: The slope's t is ≥ 2 and the supporting check passes (the mean unusual move is > 0).
- Reject: The slope's t is ≤ -2: larger scaled rises are followed by smaller or reversing 5-day moves.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a t ≥ 2 with a mean unusual move ≤ 0. The test also needs at least 100 grid cases with forecast > 0 across all coins; fewer is inconclusive.
