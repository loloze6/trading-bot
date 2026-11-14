---
idea: 002-01_sma-golden-cross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short moving average of close crossed above the long one -> adapted: "after the cross" becomes "while the short SMA is above the long one", graded by the size of the spread.
- Comparison: compared with random bars -> kept: compared with the coin's mean forward return over all the test's windows.
- Outcome: price keeps rising, more often and further -> kept: forward return of the coin, upward side only.
- Verdict transfer: yes: a long position graded by the 50/200 SMA spread earns above holding exactly when price rises more after up-crosses than at random bars, and fails to when it does not.
Forecast: The forecast uses the percent spread between the 50-day SMA and the 200-day SMA of the close, which is the conventional daily golden cross. The spread is standardised against its own last 200 values, so an average spread is about 10. It is then clipped at 0. The forecast is positive and grows with the spread while the 50-day SMA is above the 200-day SMA. It is zero while the 50-day SMA is below the 200-day SMA, because the idea concerns upward crosses only. The forecast is capped at 20.
Config: 002-01_sma-golden-cross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Regress the coin's forward 10-bar return on the forecast, pooled over coins and windows. Use non-overlapping 10-bar samples and subtract the coin's mean 10-bar return over all windows together (holding) from each forward return.
- Supporting check: On bars with forecast > 0, the share of positive forward 10-bar returns minus the share of positive 10-bar returns over all bars of that coin (all windows).
- Confirm: The slope is positive with t >= 2, counting each non-overlapping block once.
- Reject: The slope is negative with t <= -2 (gains fall as the position grows, so moves after up-crosses reverse).
- Inconclusive: Any t between -2 and 2, including an estimate near zero or merely negative. The result is also inconclusive if there are fewer than 100 non-overlapping blocks with forecast > 0.
