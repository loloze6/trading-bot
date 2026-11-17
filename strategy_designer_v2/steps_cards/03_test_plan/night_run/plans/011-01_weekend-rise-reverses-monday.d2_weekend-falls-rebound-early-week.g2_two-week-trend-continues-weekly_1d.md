---
idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the coin's 14-day return scaled by its 20-day volatility -> kept
- Comparison: none
- Outcome: a move in the same direction over the next 7 days, larger the larger the scaled return -> kept
- Verdict transfer: yes: the forecast is the idea's own scaled return, with its 14- and 20-day durations, measured against the 7-day forward return.
Forecast: The forecast is VolatilityScaledReturnComponent with period 14 and vol_period 20. It is the 14-bar return divided by the standard deviation of the last 20 daily returns times sqrt(14). It is standardised against its own past 60 values (min_periods 20), so its average absolute value is about 10, capped at ±20. The forecast is positive after a 14-day rise and negative after a 14-day fall. It is near zero when the scaled return is small and grows linearly with the scaled return. It is ungated and active on every bar, long and short.
Config: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use non-overlapping 7-bar cases (positions 0, 7, 14, ... of each window). For each case, take the forecast at bar t times the excess return, which is close[t+7]/close[t] − 1 minus that coin's mean 7-bar return over all windows. Pool these products over all coins and windows and compute the t-statistic of their mean.
- Supporting check: Split the book's mean daily return before costs into market rise and timing (book mean minus position × the coin's mean daily return over all windows). The timing part must be above 0.
- Confirm: The pooled mean of the product is positive with t ≥ 2, and the timing part of the book's mean daily return is above 0.
- Reject: The pooled mean of the product is negative with t ≤ −2 (fading the two-week trend wins).
- Inconclusive: Any t between −2 and 2 is inconclusive. A t ≥ 2 with a timing part ≤ 0 is also inconclusive. At least 300 independent 7-bar cases are required in total, else inconclusive.
