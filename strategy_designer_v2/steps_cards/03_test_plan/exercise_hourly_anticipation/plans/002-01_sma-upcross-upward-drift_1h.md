---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short average has crossed above long average -> adapted: "after the cross" made "while short SMA is above long SMA", graded by the spread between them.
- Comparison: random points -> adapted: all bars of the same window, that is, simply holding the coin.
- Outcome: price keeps rising, more often and further -> kept: forward returns while long versus unconditional forward returns.
- Verdict transfer: yes: the spread is positive exactly from an upward cross until the next downward cross, so excess forward returns while it is positive are the idea's persistence.
Forecast: The forecast is the percent spread between the 50-bar SMA and the 200-bar SMA of the close. These are the conventional cross settings, since the brief gives none. The spread is standardised against its own past 200 values (average absolute value about 10, capped at 20) and clipped at 0, because the idea concerns upward crosses only. It is zero while the short SMA is below the long one. It is positive from the upward cross onward, and it grows as the short average pulls further above the long one.
Config: 002-01_sma-upcross-upward-drift_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The mean forward 24-bar close-to-close return on bars where the forecast is above 0, minus the mean forward 24-bar return over all bars of the same window (holding the coin). Bars are sampled every 24 bars so returns do not overlap, and the six windows are pooled.
- Supporting check: The share of positive forward 24-bar returns when the forecast is above 0, minus the same share over all bars.
- Confirm: The pooled excess mean return is above 0 with t ≥ 2, and it is positive in at least 4 of the 6 windows.
- Reject: The pooled excess is at or below 0. A t ≤ -2 means moves after up-crosses reverse.
- Inconclusive: The excess is positive but t < 2, or it is positive in fewer than 4 windows. At least 100 non-overlapping 24-bar blocks with forecast above 0 are needed across the windows; with fewer, the result is inconclusive.
