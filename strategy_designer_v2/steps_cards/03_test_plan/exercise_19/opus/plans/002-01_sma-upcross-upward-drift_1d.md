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
- Situation: short SMA has crossed above long SMA -> adapted: "after the cross" made "while short is above long", graded by the SMA50/SMA200 percent spread.
- Comparison: forward moves after random points -> kept: the regression intercept and the all-bars mean act as the random-point baseline.
- Outcome: price keeps rising over the following bars -> kept: BTC's forward 10-bar close-to-close return.
- Verdict transfer: yes: forward returns that grow with the spread above zero confirm persistence after up-crosses, and flat or reversing returns reject it.
Forecast: The indicator is the spread (SMA50 − SMA200) / SMA200 × 100 on daily closes. These are the conventional golden-cross settings. The spread is standardised against its own past 200 values (min_periods 50), then clipped at 0, so the forecast is long-only. The forecast is 0 while SMA50 is below SMA200. It starts at about 0 at an upward cross and grows smoothly as the short average pulls further above the long one, capped at +20.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Slope (with its t-stat) of BTC's forward 10-bar log return regressed on the forecast. Use non-overlapping 10-bar blocks pooled over the 6 windows, before costs. The intercept carries buy-and-hold drift, so the slope is the gain beyond holding or a random point.
- Supporting check: Share of positive forward 10-bar returns when the forecast is above 0, against the share over all bars.
- Confirm: Slope t ≥ +2, with the hit-rate share above the all-bars share.
- Reject: Either of two results rejects the idea: - Reversal: slope t ≤ −2. - No difference (equivalence test): the whole 90% confidence interval of the slope lies inside ±0.05% of 10-bar return per forecast point (±0.5% per full position).
- Inconclusive: Any slope with |t| < 2 whose 90% confidence interval is not inside the band is inconclusive. The result is also inconclusive with fewer than 30 non-overlapping 10-bar blocks having forecast > 0 across all windows.
