---
idea: 010-01_rsi-above-share-continuation
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 69355866607f
---
Fidelity:
- Situation: share of the past 30 days that the 14-day RSI spent above 50 -> kept
- Comparison: a larger share against a smaller share -> kept
- Outcome: higher coin return over the next 14 days -> kept
- Verdict transfer: yes: the forecast is the RSI-above-50 share itself, and the test checks whether the next 14-day return rises with it.
Forecast: The indicator is the share of the last 30 daily bars on which the 14-day RSI was above 50, minus 0.5. It runs from -0.5 (RSI was never above 50) to +0.5 (always above), in steps of 1/30. The share is standardised against its own past 130 values, so its average absolute size is about 10. The forecast is positive (long) when RSI held above 50 on more than half of the 30 days, and negative (short) when it held above 50 on fewer than half. It is zero at exactly half. The position grows in step with how far the share sits from one half. There is no regime: the forecast is active on every bar.
Config: 010-01_rsi-above-share-continuation_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: The bar-t forecast is regressed against the next 14-bar excess return. The excess return is close[t+14]/close[t] - 1 minus that coin's mean 14-bar return over all windows. Samples are non-overlapping (positions 0, 14, 28, ... in each window), and all coins and windows are pooled. The measure is the t-statistic of the slope.
- Supporting check: The mean excess 14-bar return of samples with forecast > 0, minus the mean of samples with forecast < 0, must be above 0 (on the same samples).
- Confirm: The slope t-statistic is ≥ +2 and the supporting check passes (difference > 0).
- Reject: The slope t-statistic is ≤ -2, meaning returns run against the side RSI has held.
- Inconclusive: A slope t-statistic between -2 and +2, or t ≥ 2 with a check difference ≤ 0, is inconclusive. A result near zero is inconclusive, not a reject. At least 300 independent 14-bar samples are required; about 576 are expected (24 windows × 8 × 3 coins).
