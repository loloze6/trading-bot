---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 91c94c46188e
---
Fidelity:
- Situation: a down day whose volume is heavy against the prior 20-day average -> adapted: both conditions are kept as a regime rule, and inside it the position grows with the volume ratio.
- Comparison: a larger remaining share of the fall (a small lower wick against the range), more so when 20-day volatility is high -> kept: (high - close)/(high - low), scaled by the 20-day volatility against its 60-day mean.
- Outcome: the coin rises over the next day -> kept: long for 1 daily bar.
- Verdict transfer: yes: the forecast is long on heavy-volume down days in proportion to the unbounced share of the fall, its volume and its volatility, and is measured on the next day's return.
Forecast: On days that close below the prior close with volume at or above its prior 20-day mean, the forecast is long. Its size is the product of three parts: the close's distance below the day's high as a share of the range, the day's volume over its prior 20-day mean, and the 20-day return volatility over its 60-day mean. That product is standardised over its last 80 values, so a typical case is about +10. It is 0 when the close sits at the day's high. It is flat on every other day. It never goes short.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, take each case's forecast x (next-day return minus the coin's mean daily return over all windows). Measure the mean of these values and its t across cases (one case per bar, since the horizon is 1 bar).
- Supporting check: The mean excess next-day return of cases above the median forecast minus that of cases below it is > 0.
- Confirm: The main measure's t is ≥ 2 and the supporting check is > 0.
- Reject: The main measure's t is ≤ -2.
- Inconclusive: A t between -2 and 2, or a t ≥ 2 while the check fails, is inconclusive. Fewer than 200 cases with forecast > 0 is also inconclusive.
