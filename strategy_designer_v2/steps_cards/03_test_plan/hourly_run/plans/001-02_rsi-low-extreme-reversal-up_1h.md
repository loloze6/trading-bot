---
idea: 001-02_rsi-low-extreme-reversal-up
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: hourly RSI at a low extreme after a one-sided drop -> adapted: graded RSI below 50, amplified toward extremes by a soft dead zone.
- Comparison: returns after extreme readings vs after neutral readings -> kept: the criterion compares forward returns of top-forecast bars with zero-forecast bars.
- Outcome: price rises over the next hours, recovering part of the drop -> adapted: the position is held while RSI stays low, with no fixed holding period.
- Verdict transfer: yes: the forecast is large exactly at low RSI extremes and zero otherwise, so its forward returns answer the idea directly.
Forecast: Use the 14-bar Wilder RSI pullback, (50 - RSI), with both signs. Standardise it against its own past 60 values, so a typical reading is about 10. Clip it at 0, which keeps only RSI below 50 and makes the test long only. Then apply signed_power (exponent 2, pivot 10): mild oversold readings shrink toward 0 and deep extremes grow, up to the +20 cap. The forecast is 0 when RSI is 50 or higher. It is small for RSI in the 40s and grows smoothly as RSI falls toward its extremes.
Config: 001-02_rsi-low-extreme-reversal-up_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The 24-bar forward return of the coin after bars in the top decile of forecast, minus its forward return after bars where the forecast is 0 (neutral or high RSI). Pool all coins and windows, count overlapping 24-bar returns once (non-overlapping sampling or Newey-West, lag 24), and compute the t-statistic. This is before costs.
- Supporting check: The portfolio return per unit of average exposure, minus the coin's buy-and-hold return over the same bars, must be positive in at least 2 of the 3 coins.
- Confirm: The top-decile minus neutral forward return is positive with t ≥ 2, and the supporting check holds.
- Reject: The top-decile minus neutral forward return is negative with t ≤ -2, meaning continuation rather than recovery. A |t| < 2 with at least 150 cases also rejects the idea's predictive claim as stated, but only if the estimate is within ±0.1% per 24 bars, which is no difference from neutral readings.
- Inconclusive: Any |t| < 2 that does not meet the near-zero bound above, or the supporting check failing alongside t ≥ 2. Fewer than 150 non-overlapping top-decile cases in the pool is too few for any verdict.
