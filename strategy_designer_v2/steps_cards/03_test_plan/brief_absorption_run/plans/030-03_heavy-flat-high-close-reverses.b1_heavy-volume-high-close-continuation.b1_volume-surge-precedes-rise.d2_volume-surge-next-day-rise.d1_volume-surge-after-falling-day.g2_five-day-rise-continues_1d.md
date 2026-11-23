---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 91c94c46188e
---
Fidelity:
- Situation: a coin's 5-day rise, measured in its usual 5-day moves -> kept
- Comparison: the larger the rise, the larger the next move -> kept
- Outcome: the coin rises over the next 3 days -> kept
- Verdict transfer: yes: the forecast is the 5-day rise in usual 5-day moves, long only, and the test reads the next 3 days' return against it.
Forecast: The forecast uses MeanAbsScaledReturnComponent with period 5 and window 365. This is the 5-day return divided by the mean absolute 5-day return over the past year (365 bars). It is standardised against its own past 370 values and clipped at 0. The forecast is positive after a 5-day rise and grows in proportion to the rise's size in usual 5-day moves, up to the cap of 20. It is zero after a flat or falling 5 days. It is never short, because the idea makes no claim about falls.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use bars on a non-overlapping 3-bar grid in each window, pooled over coins and windows, where the forecast is above 0. On those bars, regress the coin's 3-bar forward return minus its normal 3-bar drift on the forecast (`post_pipeline_value` of rise5). The drift is the coin's mean 3-bar return over all windows. The measure is the slope and its t.
- Supporting check: The forecast-weighted mean of the same excess 3-bar return, over the same cases, is above 0.
- Confirm: The slope is positive with t >= 2.0 and the supporting check passes.
- Reject: The slope is negative with t <= -2.0.
- Inconclusive: Any t between -2.0 and 2.0, or a confirming t with a failed supporting check. Fewer than 200 grid cases with a positive forecast is inconclusive whatever the t.
