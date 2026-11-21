---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: a coin's 7-day return is among its largest -> adapted: the "among its largest" threshold is made graded, as the 168-bar return scaled to its own past size with a cubic dead zone.
- Comparison: the rise against its usual 7-day drift -> kept
- Outcome: over the next 7 days it rises more, and more the larger the week's rise -> kept
- Verdict transfer: yes: the forecast is long in proportion to the strength of the week's rise, held for 7 days, and judged against the coin's normal 7-day drift.
Forecast: One component, the 168-bar (7-day) percent return of the close (PriceEvolutionComponent, period 168). It is standardised against the mean absolute size of its previous 168 values (window 168, min_periods 42), so a usual week reads about ±10. It is clipped at 0, so only rising weeks count. It then goes through signed_power with exponent 3 and pivot 10, the strongest graded dead zone the guide allows. An ordinary up-week of about +5 gives about +1.25, so the position is near flat. A week at twice its usual size (+20) gives +80, which the final clip caps at +20. The forecast is zero when the 7-day return is not positive. It is never negative, and it grows steeply and continuously with the size of the week's rise.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e2_strong-week-keeps-rising_1h_config.json
Criterion:
- Horizon: 168 bars
- Main measure: The cases are bets: rises of the forecast of at least 2 points, read once per non-overlapping 168-bar grid cell of each window. For each case, take the coin's return over the next 168 bars minus its normal 168-bar drift, which is its mean 168-bar return over all windows. The measure is the mean of this unusual move over the cases, with its t-statistic.
- Supporting check: Over the grid cells with a case, the slope of the unusual move regressed on the forecast at the signal bar is positive.
- Confirm: The mean unusual move is positive with t ≥ 2, over at least 30 cases, and the supporting slope is above 0.
- Reject: The mean unusual move is negative with t ≤ -2, over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a main measure at t ≥ 2 with a slope at or below 0. So is any result from fewer than 30 cases pooled over the coins and windows.
