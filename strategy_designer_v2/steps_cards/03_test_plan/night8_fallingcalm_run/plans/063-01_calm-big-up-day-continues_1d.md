---
idea: 063-01_calm-big-up-day-continues
brief: 063_calm-market-big-day-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6002f52a0948
---
Fidelity:
- Situation: a coin's one-day rise in a calm market -> kept: the one-day return, clipped at 0 so only up days count; the calm profile is added by code
- Comparison: against its usual daily swing, the 30-day std of daily returns -> kept: VolatilityScaledReturnComponent with vol_period 30
- Outcome: the larger that scaled rise, the larger the rise over the next 5 days -> adapted: "the larger" is made graded, with the position growing with the scaled rise, and the book holds for 5 bars
- Verdict transfer: yes: the forecast is the scaled rise itself inside the calm profile, so the gains growing with its size confirm the idea, and the gains falling with its size reject it.
Forecast: The forecast is the day's return divided by the standard deviation of the last 30 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 30). This is standardised against its own past 60 values (min_periods 20) and clipped at 0. It is 0 on down and flat days, positive on up days, and grows linearly with the size of the rise in usual daily moves, up to +20. It is never negative. Outside the calm profile, code keeps it at 0.
Config: 063-01_calm-big-up-day-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: On in-profile bars of a non-overlapping 5-bar grid per window, take each coin's 5-bar forward return minus that coin's mean 5-bar return over all windows (the drift of holding it). Regress this excess return on the forecast (post_pipeline_value of scaled_rise). Report the slope's t and the number of grid cases.
- Supporting check: Take the mean excess 5-bar return over grid cases with forecast at or above 10. It must be above 0.
- Confirm: The slope's t is 2 or more, and the supporting mean is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a t of 2 or more when the supporting mean is not above 0. The test needs at least 100 grid cases with a forecast above 0, else it is inconclusive.
