---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: the coin's 30-day return is positive -> kept: a regime rule on the raw 720-bar return being above 0.
- Comparison: the larger the 7-day return, the higher the next return -> kept: the forecast grows with the 168-bar return.
- Outcome: a higher return over the next 7 days, upward -> kept: the 168-bar forward return; long only, since the consequence says a weak week means staying out.
- Verdict transfer: yes: the test measures the idea's own condition, its own graded driver and its own horizon.
Forecast: The forecast is zero on any bar where the coin's 720-bar (30-day) return is 0 or below; that regime is null. While the 720-bar return is positive, the forecast is the coin's 168-bar (7-day) percent return, standardised over its own past 169 values (minimum 42). It is then clipped at 0. So the forecast is zero after a falling week and positive after a rising one. It grows in proportion to the size of the week's rise, capped at +20. It is never negative.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h_config.json
Criterion:
- Horizon: 168 bars
- Main measure: Use the bars where the regime is trending, on the non-overlapping 168-bar grid of each window, pooled over coins and windows. On those bars, take the coin's forward 168-bar return minus that coin's mean 168-bar return over all windows. Regress it on the raw 7-day return (`week.last_history_value`) with OLS, and use the t of the slope.
- Supporting check: On trending grid bars, the mean excess forward return of bars with forecast > 0, minus that of bars with forecast = 0, must be above 0.
- Confirm: The slope's t is 2 or more, and the supporting difference is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2 is inconclusive. A t of 2 or more is also inconclusive when the supporting difference is 0 or below. Any result is inconclusive with fewer than 100 trending grid cases, or fewer than 30 on each side of the forecast-zero split.
