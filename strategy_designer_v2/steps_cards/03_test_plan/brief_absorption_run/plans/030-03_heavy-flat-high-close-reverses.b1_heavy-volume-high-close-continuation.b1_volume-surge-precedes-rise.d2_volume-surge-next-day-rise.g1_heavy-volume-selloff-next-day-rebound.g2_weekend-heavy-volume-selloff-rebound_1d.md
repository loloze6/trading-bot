---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g2_weekend-heavy-volume-selloff-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 91c94c46188e
---
Fidelity:
- Situation: a fall on a Saturday or Sunday whose volume is heavy against its prior 20-day average -> adapted: "heavy" is graded as the day's fall in percent times volume over the prior 20-day mean, with the weekend kept as a regime.
- Comparison: the same fall on a weekday -> kept: the same graded measure runs in a separate weekday regime.
- Outcome: the coin rises over the next day, more after weekend falls -> kept: next-bar return on 1d bars.
- Verdict transfer: yes: the weekend rebound slope and its excess over the weekday slope are measured directly, so a confirm or reject carries over to the idea.
Forecast: The forecast uses one measure, FallVolumeVolatilityWeightedComponent with volume_period 20, vol_period 20 and base_vol_period 20. Because the two volatility windows are equal, its volatility ratio is exactly 1. The measure is then the day's fall in percent times the day's volume over the mean of the prior 20 days' volumes. It is 0 on up days and grows with both the fall and the volume. It is standardised over 60 bars, so a typical value is about +10. WeekdayComponent reads the weekday of the coming bar. When that bar is a Sunday (6) or a Monday (0), the current bar is a Saturday or Sunday, and the regime is mean_reversion, which holds the measure under id "fall_we". Every other bar is the regime unknown, which holds the same measure under id "fall_wd". The forecast is never negative: it is zero on up or flat days, and the long position grows with the fall times the volume ratio.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g2_weekend-heavy-volume-selloff-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On weekend-regime bars with forecast > 0, regress the next-day return minus the coin's mean daily return (all windows) on the forecast, and read the slope's t. Before costs.
- Supporting check: The weekend slope minus the weekday slope, from the same regression on unknown-regime bars with forecast > 0, Welch-style t of the difference ≥ 2.
- Confirm: The weekend slope has t ≥ 2 and the weekend-minus-weekday slope difference has t ≥ 2.
- Reject: The weekend slope has t ≤ -2, or the weekend-minus-weekday slope difference has t ≤ -2.
- Inconclusive: Any other result, including slopes near zero, is inconclusive. A verdict needs at least 200 weekend cases and 200 weekday cases with forecast > 0.
