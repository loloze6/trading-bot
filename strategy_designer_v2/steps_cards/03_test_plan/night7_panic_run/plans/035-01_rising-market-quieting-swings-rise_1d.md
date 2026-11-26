---
idea: 035-01_rising-market-quieting-swings-rise
brief: 035_calming-swings-lift-rising-coins
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin in a rising market whose 14-day swings are low against the 90 days before -> adapted: the rising market is the profile (added by code), and the quieting is graded inside it
- Comparison: std of daily returns over the last 14 days vs the 90 days before them -> kept: recent-to-prior volatility ratio, 14 against 90 lagged 14, centred at equal volatility
- Outcome: the coin rises over the next 3 days, more the calmer the swings -> kept: long position, held 3 bars, sized by the quieting
- Verdict transfer: yes: the forecast is the idea's own ratio, inside the idea's own profile, held for its own horizon.
Forecast: The forecast uses RecentToPriorVolatilityRatioComponent with vol_period 14, base_period 90, base_lag 14 and form "centred". This is the std of the last 14 daily returns over the std of the 90 daily returns before them, minus 1. It is standardised over its own past 105 values, then negated, then clipped at 0. The forecast is positive when the recent 14 days swing less than the prior 90. It grows as they quiet further, up to the cap of 20. It is zero at equal or widening swings, because the idea claims less rise or none there, not a fall. Code keeps the book flat outside the rising profile.
Config: 035-01_rising-market-quieting-swings-rise_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Use the 3-bar forward return on a non-overlapping grid of 3 bars per window. Subtract the coin's mean 3-bar return over all its windows. Take the forecast-weighted mean over grid bars with forecast > 0. Compute its t with the cases of one day pooled.
- Supporting check: Inside the rising profile on the same grid, compare two groups by their mean excess 3-bar return. The first group is bars whose forecast is above the median of the positive forecasts. The second is bars with forecast 0 (widening swings). The difference (first minus second) must be > 0.
- Confirm: The main measure is positive with t ≥ 2 and the supporting difference is > 0.
- Reject: The main measure is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or a confirming t with a supporting difference ≤ 0. At least 60 positive-forecast grid cases, spread over at least 30 distinct days, are needed for any verdict.
