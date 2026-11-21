---
idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin has risen over the past 3 days -> kept: the 72-bar residual reads exactly 0 on bars where the 72-bar net return is not positive.
- Comparison: the share of that rise carried by its few biggest hourly gains -> kept: share of the 72-bar rise carried by the 3 largest one-bar gains, read as 1 minus that share.
- Outcome: a larger share gives a smaller further rise over the next 3 days, scaled down long, not short -> kept: a long-only position grows as the share shrinks, judged on the 72-bar forward return.
- Verdict transfer: yes: the forecast measures the stated share on the stated window and is sized against the stated 3-day outcome, so a confirm or reject carries over to the idea.
Forecast: One component, TopGainsShareOfRiseComponent (period 72, k 3, form "residual"), on every bar with no regime gate. It is 0 when the past 72 hours did not rise. When they did rise, it equals 1 minus the share of that rise carried by the 3 largest hourly gains. It is standardised against its own past 73 values. The forecast is therefore never negative, so the strategy is long-only. It is largest when a 3-day rise was a grind of many small up-hours. It shrinks towards 0 as the 3 biggest hours carry more of the rise. It is 0 when they carry all of it, and 0 after no rise.
Config: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The sample is the non-overlapping 72-bar grid of each window. Keep only grid bars whose past 72-bar return, recomputed from close, is above 0. On those bars, regress the next 72-bar return minus the coin's mean 72-bar return over all windows on the raw residual (`grind.last_history_value`). Pool all coins. Report the slope's t and the number of cases.
- Supporting check: none
- Confirm: The slope is positive with t >= 2.0. This means the future excess rise grows as the share carried by the top 3 hours falls.
- Reject: The slope is negative with t <= -2.0.
- Inconclusive: Any slope with t between -2.0 and 2.0 is inconclusive, including slopes near zero. Fewer than 200 risen grid cases pooled across coins is also inconclusive.
