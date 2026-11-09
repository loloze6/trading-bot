---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Long only, and only while the 50-day simple moving average of the close is above the 200-day simple moving average. That is the stretch that runs from an upward cross until the next downward cross. The raw value is (SMA50 − SMA200) / SMA200 × 100, using the averages as of each bar's close with the current close included. It is divided by the mean absolute value of its own previous 200 values and multiplied by 10, capped at 20. It is then clipped at 0. So the forecast is zero whenever SMA50 is at or below SMA200 and is never negative. Inside an up-stretch it is positive and grows smoothly with the gap between the two averages. It starts near 0 at the upward cross and returns to 0 at the downward cross.
Config: 002-05_sma-up-regime-positive-drift_config.json
Confirm: The test pools all six windows and uses non-overlapping 1-bar horizons. The main measure is the mean next-bar close-to-close return on bars where the forecast is above 0, minus the mean next-bar return over all bars, before costs. The idea is confirmed if this difference is positive with t ≥ 2 and rests on at least 100 in-stretch bars. The supporting check is the share of up bars: it must be higher inside the stretches than over all bars.
Reject: The idea is rejected if the in-stretch mean next-bar return is at or below the all-bar mean. It is rejected more strongly if it is significantly below (t ≤ −2), because that would show that returns tend to reverse after upward crosses.
Inconclusive: The test is inconclusive if the difference is positive but t < 2. It is also inconclusive if fewer than 100 bars fall inside up-stretches, or if all the in-stretch bars come from a single cross episode.
Deviation: The idea treats every bar between the crosses alike. The config instead sizes the position by how far SMA50 sits above SMA200, so bars just after a cross get small positions. The confirm and reject measures use the stretch membership itself (forecast above 0), not the size of the position. The test covers only up-crosses on BTC with the conventional 50/200 settings, because the brief gives none. Cross-of-price-over-long-average variants and down-crosses are not tested.
