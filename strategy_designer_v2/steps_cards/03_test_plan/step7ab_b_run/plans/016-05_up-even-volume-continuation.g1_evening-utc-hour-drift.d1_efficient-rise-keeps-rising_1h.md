---
idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin has risen over its past 3 days, measured by how efficiently -> kept: the 72-bar efficiency ratio, taken only while the 72-bar return is above zero.
- Comparison: the 3-day rise against the sum of its absolute hourly moves -> kept: the efficiency ratio, unsmoothed with smooth_period 1.
- Outcome: the more efficient the rise, the more it keeps rising over the next 3 days -> kept: long, sized by efficiency, held 72 bars.
- Verdict transfer: yes: the forecast is the idea's own efficiency measure on rises, and its gain over the next 72 bars is the idea's claim.
Forecast: When the 72-bar return is positive, the detector picks "trending". There the forecast is the 72-bar efficiency ratio, standardised (window 73, min_periods 20): |close − close 72 bars ago| divided by the sum of the 72 absolute hourly changes. It is about +10 at the usual efficiency, higher for a steadier rise, and capped at 20. On all other bars the forecast is 0. It is never negative. At the switch it is continuous, because the efficiency ratio goes to 0 as the 3-day return goes to 0.
Config: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use a non-overlapping 72-bar grid in each window. On grid bars with forecast > 0, compute (forecast/10) × (the coin's 72-bar forward return minus its mean 72-bar return over all windows). Take the mean and its t over the cases, before costs.
- Supporting check: Among those cases, the slope of the excess forward return on the forecast (OLS) is positive.
- Confirm: The main measure has t ≥ 2 and the slope estimate is above 0.
- Reject: The main measure has t ≤ -2.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with a slope at or below 0. Also any result with fewer than 200 positive-forecast grid cases across all coins and windows.
