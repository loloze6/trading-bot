---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a down day whose volume is heavy against its prior 20-day average, the fall being large -> kept: the day's fall times its volume over the 20-day mean; it is 0 on up days.
- Comparison: volume against the coin's own prior 20-day average -> kept: the 20-day mean volume, though the component's base includes the current day.
- Outcome: the coin rises over the next day, more so the heavier and deeper the down day -> kept: next-day return, long only, sized by the fall times the volume ratio.
- Verdict transfer: yes: the forecast is the idea's interaction, measured on the next day's rise.
Forecast: The forecast uses VolumeWeightedScaledReturnComponent with vol_period 20 and volume_period 20. It is the day's return in usual one-day moves times the day's volume over its 20-day mean. The value is negated, so a fall reads positive, then standardised over 60 past values and clipped at 0. It is positive only on down days and grows with both the size of the fall and the volume surge. It is 0 on up days and flat days, and it is never negative.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, take the next-day return minus the coin's mean daily return over all its windows. The measure is the forecast-weighted mean of that excess return, with its t, pooled over coins and windows.
- Supporting check: Split the forecast > 0 bars at their median forecast. The upper half's mean next-day excess return minus the lower half's must be above 0.
- Confirm: The forecast-weighted mean excess return is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The forecast-weighted mean excess return is below 0 with t ≤ -2.
- Inconclusive: These results neither confirm nor reject: - t between -2 and 2; - t ≥ 2 but the upper half does not beat the lower half; - fewer than 200 bars with forecast > 0.
