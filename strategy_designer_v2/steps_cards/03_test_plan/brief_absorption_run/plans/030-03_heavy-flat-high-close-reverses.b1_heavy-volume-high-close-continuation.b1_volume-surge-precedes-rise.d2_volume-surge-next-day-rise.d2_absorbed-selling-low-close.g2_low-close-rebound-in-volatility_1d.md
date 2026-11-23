---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 91c94c46188e
---
Fidelity:
- Situation: a day that closed near its low -> kept: (high - close) / (high - low) of the day, graded from 0 at the high to 1 at the low.
- Comparison: the higher the coin's 20-day daily volatility, the stronger -> kept: the location is multiplied by the std of the last 20 daily returns.
- Outcome: the coin rises over the next day -> kept: long, horizon 1 daily bar.
- Verdict transfer: yes: the forecast is exactly the low-close reading scaled by 20-day volatility, judged on the next day's rise.
Forecast: The forecast uses CloseLocationTimesVolatilityComponent with vol_period 20. Its raw value is the day's close-near-low share times the 20-day std of daily returns. It is standardised against its own past 60 values (min 20), which gives about +10 on an average day and is capped at 20. The forecast is never negative. It is 0 when the day closed at its high. It grows as the close nears the low and as volatility rises, so the position is largest on low closes in volatile stretches and small on low closes in calm ones.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Pool every bar of every coin and window. Regress the next-day return, minus that coin's mean daily return over all windows, on the bar's forecast (post_pipeline_value). Read the slope's t.
- Supporting check: Take bars whose close sat in the lower half of the day's range, recomputed from prices. Compare those in the top half of their coin's 20-day volatility with those in the bottom half, using the same excess next-day return: the mean of the high-volatility group minus the mean of the low-volatility group must be above 0 (Welch t ≥ 2).
- Confirm: The slope's t is 2 or more and the supporting check's Welch t is 2 or more, before costs.
- Reject: The slope's t is -2 or less, or the supporting check's Welch t is -2 or less.
- Inconclusive: Any other result, including slopes near zero. At least 1000 bars are needed in the regression and at least 200 in each volatility group, or the result is inconclusive.
