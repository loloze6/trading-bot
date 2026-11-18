---
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the close sits above the highest high of the prior 20 days -> kept
- Comparison: the distance above that high, as a share of the high -> kept
- Outcome: price rises further over the next 10 days, the larger that distance -> adapted: the holding period is dropped, so the position is held only while the close stays above the prior high, and the 10-day rise is measured on the record.
- Verdict transfer: yes: the forecast is the idea's own graded distance above the prior 20-day high, and the 10-bar forward return is read directly from the record.
Forecast: One indicator, DistanceFromHighComponent with period 20, source "high", exclude_current 1, extreme "high" and form "percent". It computes (close − highest high of bars t−20..t−1) / that high × 100. It is standardised over its past 60 values, and a clip at min 0 keeps only the part above the high. The forecast is zero while the close is at or below the prior 20-day high. It is positive when the close clears that high, and it grows in proportion to how far the close sits above it, up to the cap of 20. It is never negative.
Config: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window and keep the samples with forecast > 0. Regress the coin's 10-bar forward return minus that coin's mean 10-bar return over all windows on the forecast. The measure is the slope's t, with the number of cases stated.
- Supporting check: The mean of that excess 10-bar return over the forecast > 0 samples is above 0.
- Confirm: The slope's t is +2 or more on at least 30 cases, and the supporting check passes.
- Reject: The slope's t is −2 or less on at least 30 cases.
- Inconclusive: The idea is neither confirmed nor rejected if the slope's t is between −2 and +2, or if the t is +2 or more but the mean excess return is not above 0. It is also inconclusive with fewer than 30 forecast > 0 grid samples.
