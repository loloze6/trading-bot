---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA has crossed above the long SMA -> adapted: "after the cross" becomes "while SMA50 is above SMA200", graded by the gap between them.
- Comparison: random points -> kept: in-position bars are compared with all bars, which amounts to holding the coin.
- Outcome: price keeps rising over the following bars -> kept: the forward return of BTC over the horizon, long side.
- Verdict transfer: yes: "after a cross" made "while crossed" is an allowed adaptation, and persistence must show as better forward returns while the short average stays above the long one.
Forecast: Uses the 50-day SMA minus the 200-day SMA, as a percent of the 200-day SMA (EMASpreadComponent with average "sma"). This spread is standardised against its own past 200 values and clipped at 0. The forecast is positive, and grows with the spread, while SMA50 is above SMA200. It is zero while SMA50 is below SMA200. It is never short, because the idea is only about the upward cross.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Take the BTC 20-bar forward return at bars where the forecast is above 0, minus the mean 20-bar forward return over all bars of the same windows. Sample at non-overlapping 20-bar steps and pool the 6 windows.
- Supporting check: Across the in-position samples, the rank correlation between forecast size and the 20-bar forward return is above 0.
- Confirm: The excess forward return is above 0 with a t-stat of at least 2. The share of positive 20-bar returns while in position is also above the all-bar share. The excess is positive in at least 4 of the windows that hold positions.
- Reject: The excess forward return is at or below 0 with a t-stat of -1 or lower (moves fade or reverse after crosses). Or the excess is not above 0 in a majority of the windows that hold positions.
- Inconclusive: Any result between these two counts as inconclusive. So does a run with fewer than 10 non-overlapping in-position 20-bar samples, or fewer than 3 windows with any position.
