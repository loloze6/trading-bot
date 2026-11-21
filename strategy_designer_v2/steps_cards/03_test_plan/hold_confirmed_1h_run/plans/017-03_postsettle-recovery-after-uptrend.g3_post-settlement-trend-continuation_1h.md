---
idea: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: the 2 hours after the 16:00 UTC settlement, with the coin's own 3-day return -> kept
- Comparison: none -> kept
- Outcome: over those 2 hours the price moves with the 3-day return, more when that return is larger -> kept
- Verdict transfer: yes: the test holds a position with the 3-day return's sign and size only during the two hourly bars that start at 16:00 and 17:00 UTC, and judges their 2-bar return.
Forecast: A clock regime is active on the bars whose coming bar starts at 16:00 or 17:00 UTC. That is the bars stamped 15:00 and 16:00, so the position is held from 16:00 to 18:00. On those bars the forecast is the coin's 72-bar (3-day) percent return. It is standardised against the mean absolute value of its previous 72 hourly values (×10, capped at ±20). The forecast is positive after a 3-day rise and negative after a 3-day fall, and it grows with the size of that return. On every other hour the forecast is 0 (flat).
Config: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Take one case per day: the bar stamped 15:00 UTC, which closes at 16:00. Its outcome is the 2-bar excess return, close[t+2]/close[t] - 1 minus the coin's mean 2-bar return over all windows, inside the same window only. Regress that excess return on the bar's recorded forecast, pooled across coins and windows, and test the slope with an ordinary t-statistic. Cases are 24 bars apart, so they do not overlap.
- Supporting check: Compute the mean of sign(forecast) × excess 2-bar return over the same cases. It must be above 0.
- Confirm: The slope's t is ≥ 2 and the supporting mean is above 0, from at least 1000 cases.
- Reject: The slope's t is ≤ -2: the post-settlement move runs against the 3-day return, more so when that return is larger.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a t ≥ 2 with a supporting mean ≤ 0, and so is a result from fewer than 1000 cases.
