---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 5c26677afd57
---
Fidelity:
- Situation: a coin's 30-day return is positive, and larger -> kept: the 720-bar return, zero when not positive, graded by its size.
- Comparison: more than its usual 2-week drift -> kept: the 336-bar return minus the coin's mean 336-bar return over all windows.
- Outcome: keeps rising over the next 2 weeks, more as the 30-day return is larger -> kept: forward 336-bar return, graded by the forecast.
- Verdict transfer: yes: the forecast is the idea's own 30-day return, held for its 2-week horizon and judged against the coin's normal 2-week drift.
Forecast: One component, PriceEvolutionOnPeriodComponent with comparison_period 720 (30 days on 1h bars), gives the 30-day percent return. It is standardised over its past 500 values (min_periods 120), then clipped at 0. The forecast is 0 when the 30-day return is zero or negative. It is positive (long) when that return is positive, and grows in proportion to the size of the rise against its usual size, capped at +20. It never goes short, because the idea makes no claim about falling coins.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h_config.json
Criterion:
- Horizon: 336 bars
- Main measure: On the non-overlapping 336-bar grid of each window, take every cell with forecast > 0. For each, compute the excess return: close[t+336]/close[t] - 1 minus the coin's mean 336-bar return over all its windows. Measure the forecast-weighted mean excess return, sum(forecast x excess) / sum(forecast), with its t over the cells.
- Supporting check: Among the same cells, the OLS slope of excess return on forecast is positive with t >= 2 (the rise grows with the 30-day return). All before costs.
- Confirm: The main measure is positive with t >= 2, and the supporting check passes (slope t >= 2), over at least 200 cells.
- Reject: The main measure is negative with t <= -2, or the slope of excess return on forecast has t <= -2, over at least 200 cells.
- Inconclusive: Any other result: either t between -2 and 2, or the main measure at t >= 2 with a slope t below 2. Also inconclusive with fewer than 200 cells with forecast > 0 (about 1150 grid cells exist across 6 coins and 24 windows, about half of them positive).
