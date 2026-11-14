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
- Situation: short average has crossed above the long average -> adapted: "after the cross" becomes "while the 50-bar SMA is above the 200-bar SMA", graded by the size of the gap.
- Comparison: versus random points -> kept: compared against simply holding the coin on all bars.
- Outcome: price keeps rising, more often and further -> kept: forward returns while the position is on.
- Verdict transfer: yes: drift that persists while the short average stays above the long one, beyond holding, is the claimed persistence after the up-cross.
Forecast: The percent spread of the 50-bar SMA over the 200-bar SMA, standardised against its own past 200 values. The forecast is positive and grows with the gap while the short average is above the long one. It is clipped at 0, so it is zero (flat) while the short average is below. The forecast is long only, because the idea concerns only the upward cross.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Mean 20-bar forward return on bars where the forecast is above 0, minus the mean 20-bar forward return on all bars (the holding baseline). Pooled over the 6 windows, with the t-statistic taken on non-overlapping 20-bar blocks.
- Supporting check: Share of positive 20-bar forward returns on bars with forecast above 0, versus the share on all bars. Also check that the excess grows from the lower half to the upper half of positive forecasts.
- Confirm: The excess is positive with t ≥ 2.
- Reject: The excess is negative with t ≤ -2, which would mean moves reverse after the up-cross.
- Inconclusive: Any t between -2 and 2. Also inconclusive if there are fewer than 10 non-overlapping 20-bar blocks with a forecast above 0.
