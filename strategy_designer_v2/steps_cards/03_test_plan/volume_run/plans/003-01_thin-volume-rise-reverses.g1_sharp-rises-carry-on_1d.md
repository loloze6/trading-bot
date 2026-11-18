---
idea: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a one-day rise larger than the coin's 20-day volatility -> adapted: the "more than one usual move" threshold is made graded, as the one-day return in 20-day volatility units, kept only when it is a rise, with a graded dead zone.
- Comparison: the rise against its usual daily move (20-day volatility) -> kept: the return is divided by the 20-bar standard deviation of daily returns.
- Outcome: price keeps rising over the next 5 days, and more after larger rises -> adapted: the 5-day hold is dropped from the position, and the 5-bar forward return is measured directly in the criterion.
- Verdict transfer: yes: the forecast grows with the rise in volatility units, and the criterion tests exactly whether the 5-day return grows with it.
Forecast: The forecast is built from `VolatilityScaledReturnComponent` (period 1, vol_period 20), which gives today's return divided by the standard deviation of the last 20 daily returns. That value is standardised against its own past 60 values (window 60, min_periods 20), so an average-sized move reads about 10. It is then clipped at 0, so down days and flat days give a forecast of 0. Finally `signed_power` (exponent 2, pivot 10) damps ordinary up days towards 0 and amplifies the large ones. The forecast is positive only after an up day, never negative, and grows with the square of the rise's size in volatility units, up to the cap of 20. It is 0 after any down day.
Config: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the non-overlapping grid of bars at positions 0, 5, 10, ... of each window. On those bars, take the coin's 5-bar forward return minus that coin's mean 5-bar return over all windows. Regress this excess return on the recorded forecast (`post_pipeline_value` of up_shock) and read the t of the slope.
- Supporting check: On grid bars where the forecast is 10 or more (a rise of about one usual move or larger), the mean excess 5-bar return is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a slope t of 2 or more when the supporting check fails. The test needs at least 150 grid cases with a forecast above 0 and at least 50 with a forecast of 10 or more; with fewer, it is inconclusive.
