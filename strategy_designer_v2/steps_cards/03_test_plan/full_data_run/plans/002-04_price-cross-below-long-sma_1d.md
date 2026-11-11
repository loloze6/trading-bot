---
idea: 002-04_price-cross-below-long-sma
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the close crosses below its long moving average -> adapted: "after the cross" becomes "while below", graded by the percent distance below the 200-day SMA.
- Comparison: falling more than after random bars -> kept: forward returns on short bars are compared with the coin's unconditional forward returns over the same window.
- Outcome: price keeps falling, more often and further -> kept: the forward return is negative relative to holding.
- Verdict transfer: yes: a downward drift that grows with the distance below the long average confirms or rejects the post-cross persistence the idea claims.
Forecast: The percent distance of the close from its 200-day SMA, which includes the current bar. It is standardised over the 200 values before the current one (min_periods 50), so a typical value is about 10. It is then clipped at a maximum of 0, so the idea's short side is the only one traded. The forecast is negative while the close is below the 200-day SMA, and grows more negative the further below it sits, up to the cap of -20. It is zero while the close is at or above the average.
Config: 002-04_price-cross-below-long-sma_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Regress the forward 20-bar return of the coin, minus that coin's mean 20-bar return in the same window (the buy-and-hold drift), on the forecast. Pool all coins and windows, and use non-overlapping 20-bar blocks or Newey-West errors with 20 lags, so overlapping returns count once. Judge before costs.
- Supporting check: On bars with forecast below 0, count the non-overlapping 20-bar periods. Measure the share in which the forward return is below the coin's median 20-bar return in that window.
- Confirm: The slope on the forecast is positive with t ≥ 2: the more negative the forecast, the lower the excess forward return. The supporting share should also be above 50%.
- Reject: The slope is negative with t ≤ -2. That means price rises relative to holding the further it sits below the average, which is the reversal or exhaustion the brief names.
- Inconclusive: Any t strictly between -2 and 2, including a slope near zero. The test is also inconclusive if there are fewer than 30 non-overlapping 20-bar periods with a non-zero forecast, pooled across coins and windows.
