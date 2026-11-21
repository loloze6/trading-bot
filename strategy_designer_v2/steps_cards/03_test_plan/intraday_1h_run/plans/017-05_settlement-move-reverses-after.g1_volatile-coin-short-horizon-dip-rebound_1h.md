---
idea: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: in a coin with high 7-day mean absolute hourly move, a 2-hour fall measured against its usual 2-hour move -> adapted: "high" becomes a regime rule (7-day mean absolute move ranks at or above the median of its last 720 hours); the fall size is graded in usual 2-hour moves.
- Comparison: the fall judged against the coin's usual 2-hour move -> kept: the 2-hour return is divided by the 7-day hourly return std times sqrt(2).
- Outcome: a rise over the next 2 hours, larger after larger falls, at any hour -> kept: the 2-bar forward return, no clock gating.
- Verdict transfer: yes: the test measures the stated volatility condition, the scaled 2-hour fall and the 2-hour rebound, so its result is the idea's result.
Forecast: The forecast is active only when the coin's 7-day (168-bar) mean absolute hourly move ranks at or above 0.5 among the last 720 hours. Otherwise the regime is null and the forecast is flat. When active, it reads the 2-bar return divided by (the 168-bar std of hourly returns x sqrt(2)). This value is standardised over the past 169 values, then negated and clipped at 0. So the forecast is positive after a fall, grows linearly with the fall's size in usual 2-hour moves (capped at 20), and is 0 after a rise. It is never negative.
Config: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The sample is bars in the mean_reversion regime on the non-overlapping 2-bar grid of each window, pooled over coins and windows. On it, regress the coin's 2-bar forward return minus that coin's mean 2-bar return over all windows on the forecast. The measure is the slope's t.
- Supporting check: The mean of that excess 2-bar return over the top quintile of positive forecasts is above 0.
- Confirm: The slope is positive with t >= 2 and the supporting check passes, with at least 300 grid bars where forecast > 0.
- Reject: The slope is negative with t <= -2, with at least 300 grid bars where forecast > 0.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is t >= 2 when the top-quintile mean is not above 0, and so is any result with fewer than 300 grid bars where forecast > 0.
