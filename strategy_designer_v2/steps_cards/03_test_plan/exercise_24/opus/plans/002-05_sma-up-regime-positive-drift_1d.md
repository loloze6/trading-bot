---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short average above long average, from the upward cross until the downward cross -> adapted: the on/off "between crosses" state becomes the graded SMA50 minus SMA200 spread, long only while it is positive.
- Comparison: random stretches of the same length -> kept: next-bar returns while positioned are compared with holding the coin over the same bars.
- Outcome: price rises more often and further over the stretch -> adapted: the stretch-level hold becomes bar-by-bar next-bar returns, with the holding period dropped.
- Verdict transfer: yes: up returns during positive spread are exactly the "between crosses" drift the idea claims, and their absence or reversal is its stated failure.
Forecast: SMA50 minus SMA200 as a percent of SMA200 (the 50/200 daily cross convention), divided by its mean absolute value over the prior 200 bars and scaled to 10. Negative values are clipped to 0. The forecast is zero from a downward cross to the next upward cross. It is positive from an upward cross until the downward cross, starting near 0 at the cross. It grows as the short average pulls further above the long one, capped at 20.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Pool all windows. Regress the coin's next-bar close-to-close return on the bar's forecast, before costs. The slope measures return beyond holding the coin at the same average exposure. Bars do not overlap at a 1-bar horizon.
- Supporting check: The share of up next-bar closes on bars with forecast > 0, against the share on all bars.
- Confirm: The slope is positive with t >= 2, and the supporting up-share is higher on forecast > 0 bars.
- Reject: The slope is negative with t <= -2, meaning moves inside upward-cross stretches reverse.
- Inconclusive: Any t strictly between -2 and 2, including a near-zero slope. The test needs at least 100 bars with forecast > 0, spread over at least 2 windows; with fewer, the result is inconclusive whatever t shows.
