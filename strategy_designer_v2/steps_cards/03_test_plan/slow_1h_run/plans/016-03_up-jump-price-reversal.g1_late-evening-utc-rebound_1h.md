---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: the coin has fallen over the 24 hours up to the 20:00 UTC close, the deeper the stronger -> adapted: the 24-bar fall is graded and active while the coming bar starts at 20:00 or 21:00 UTC, so the second hour uses the fall up to 21:00 ("after X" made "while X").
- Comparison: deeper falls against shallower ones, set by "the more ... the more" -> kept: the long size grows with the depth of the fall.
- Outcome: price rises over the next 2 hours, more after deeper falls -> kept: the 2-bar forward return from the 20:00 close is measured on the record.
- Verdict transfer: yes: the criterion reads the 2-bar return after each 20:00 close against the forecast set by that day's 24-hour fall, which is the idea's own claim.
Forecast: The regime is active only when the coming hourly bar starts at 20:00 or 21:00 UTC. It is flat at every other hour. While active, the forecast takes the coin's percent change over the last 24 hourly bars. It is standardised against its own past 60 values, sign-flipped, and clipped at 0. It is positive and grows with the depth of the 24-hour fall. It is 0 when the coin rose over those 24 hours. It is never short.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Use the decision bars only. These are the bars stamped 19:00 UTC, which close at 20:00, with one case per coin per day. On each, compute the 2-bar return close[t+2]/close[t]-1 inside its window. Subtract the coin's mean 2-bar return on the same grid over all windows. Then take the mean of forecast x excess return over all decision bars and coins, with its ordinary t.
- Supporting check: Compare decision bars in the top fifth of positive forecasts with decision bars where the forecast is 0. The difference in mean 2-bar excess return (top fifth minus zero) must be above 0.
- Confirm: The forecast-weighted mean excess return is positive with t >= 2, and the supporting difference is above 0.
- Reject: The forecast-weighted mean excess return is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive t >= 2 whose supporting difference is not above 0 is also inconclusive. The test needs at least 500 decision bars with a forecast above 0, summed over coins and windows.
