---
idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour that rises far more than its typical 30-day hourly move, on volume several times its 30-day hourly average -> adapted: the "far above" thresholds become a graded product of rise-in-usual-moves and volume ratio, cubed so that only joint extremes carry size.
- Comparison: the hour's rise against its 30-day typical move, and its volume against its 30-day average volume -> kept: 720-bar return std and 720-bar mean volume.
- Outcome: the price keeps rising over the next four hours, more the larger both ratios are -> kept: long, held 4 bars, sized by the graded product.
- Verdict transfer: yes: the forecast is long exactly on heavy-volume up-surge hours, sized by both ratios, and held for the stated four hours.
Forecast: One component, VolumeWeightedScaledReturnComponent (vol_period 720, volume_period 720). Its value is the hour's return divided by the std of the last 720 hourly returns, times the hour's volume over the 720-hour mean volume. It is standardised over its past 500 values (min_periods 120). It is clipped at 0, so only up hours count. It is then cubed with signed_power (exponent 3, pivot 10). The forecast is zero on down or flat hours. It is near zero on ordinary up hours. It grows steeply, up to the cap, only when the rise and the volume are both far above their 30-day norms. It is never negative.
Config: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h_config.json
Criterion:
- Horizon: 4 bars
- Main measure: Each case is a bet, meaning a rise of the forecast of at least 2 points, read once per non-overlapping 4-bar grid cell of each window. For each case, take the coin's 4-bar return from the signal bar's close, minus the coin's mean 4-bar return over all windows. The measure is the mean of this excess return, with its t.
- Supporting check: The forecast-weighted mean of the same excess returns is above 0, so larger surges are followed by larger rises.
- Confirm: The mean excess 4-bar return is positive with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean excess 4-bar return is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: The idea is neither confirmed nor rejected when -2 < t < 2, when t ≥ 2 but the supporting check fails, or when there are fewer than 30 cases across both coins and all windows.
