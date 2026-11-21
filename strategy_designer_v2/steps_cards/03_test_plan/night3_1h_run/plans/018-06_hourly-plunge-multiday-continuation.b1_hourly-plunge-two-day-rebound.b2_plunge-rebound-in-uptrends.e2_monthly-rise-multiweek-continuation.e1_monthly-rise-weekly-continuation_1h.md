---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5c26677afd57
---
Fidelity:
- Situation: a coin's 30-day return is positive, and larger is stronger -> adapted: the on/off "positive" condition is made graded, as the 720-bar return clipped at 0.
- Comparison: more than the coin's usual 7-day drift -> kept: the forward return minus the coin's mean 168-bar return over all windows.
- Outcome: the price rises over the next 7 days, and rises more for a larger 30-day return -> kept: the 168-bar forward return, held 168 bars.
- Verdict transfer: yes: the forecast is the idea's own 30-day return, held for its own 7 days and judged against the coin's drift, so a confirm or a reject carries over to the idea.
Forecast: One component, the 720-bar (30-day) percent return of the close (`PriceEvolutionComponent`, period 720). It is standardised against its own past 500 values (min_periods 120), then clipped at 0. The forecast is 0 while the 30-day return is zero or negative. It is positive while that return is positive, and grows in proportion to the return's size against its usual size, up to the cap of 20. There is no regime and no dead zone: the forecast rises continuously from 0 as the return turns positive.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h_config.json
Criterion:
- Horizon: 168 bars
- Main measure: Use the non-overlapping 168-bar grid of each window, pooled over coins and windows. For each grid bar, take the coin's forward 168-bar return minus its normal 168-bar drift, divided by its usual 168-bar move. Regress this on the recorded forecast, over all grid bars, including those with forecast 0. The measure is the t of that slope.
- Supporting check: On grid bars with forecast > 0, the mean drift-adjusted 168-bar return (the strength) is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes (mean strength above 0 on forecast > 0 cases).
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with mean strength at or below 0. At least 300 grid bars with forecast > 0 are needed; fewer is inconclusive.
