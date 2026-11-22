---
idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the price rises from Saturday 00:00 to Monday 00:00 UTC, while the 30-day hourly volatility is high against its last 6 months -> kept: the 48-bar return on the bar closing at Monday 00:00, and a volatility-rank regime rule
- Comparison: the 30-day volatility judged against its own last 6 months -> kept: the rank of the 720-bar volatility among its last 4320 values, at or above 0.5
- Outcome: the price falls over Monday and Tuesday, more after a larger weekend gain -> kept: a short sized by the weekend gain, held 48 bars
- Verdict transfer: yes: the test measures the idea's own weekend gain, volatility condition and two-day fall.
Forecast: The forecast is computed only on the bar whose close is Monday 00:00 UTC. On that bar the weekday clock reads 0 and the hour clock reads 0, and the 30-day volatility must rank at or above the median of the last 6 months. On every other bar it is 0. On that bar it is minus the standardised 48-bar return from Saturday 00:00 to Monday 00:00, clipped at 0. So it is short after a weekend rise, its size grows with the gain (about −10 for a typical move, down to −20), and it is 0 after a weekend fall. The short is held for the 48 bars of Monday and Tuesday.
Config: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: Each case is a bar with a nonzero forecast, which is at most one per week. For each case, take the coin's return over the next 48 bars minus its normal 48-bar drift, with the sign flipped to the short side. Average these unusual moves with each case weighted by its abs(forecast), pooled over coins and windows, and take the t of that weighted mean.
- Supporting check: Split the cases at the median of abs(forecast). The mean unusual fall of the larger half minus that of the smaller half must be above 0.
- Confirm: The weighted mean unusual fall has t ≥ 2 over at least 100 cases, and the supporting check is above 0.
- Reject: The weighted mean unusual fall has t ≤ −2 over at least 100 cases, meaning weekend rises in turbulent weeks keep rising on Monday and Tuesday.
- Inconclusive: Any t between −2 and 2 is inconclusive. So is t ≥ 2 with the size check at 0 or below, or fewer than 100 cases.
