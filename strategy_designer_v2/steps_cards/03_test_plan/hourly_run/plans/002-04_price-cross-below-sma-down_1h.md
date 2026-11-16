---
idea: 002-04_price-cross-below-sma-down
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close falls below the long moving average after being above it -> adapted: "after the down-cross" becomes "while below the SMA(200)", sized by how far the close is below it.
- Comparison: random points -> kept: forward returns on short bars are compared with the unconditional forward return of all bars.
- Outcome: price keeps falling, more often and further -> kept: forward return and the share of falls over 24 bars, short side.
- Verdict transfer: yes: a persistent downtrend after the cross must show as falling prices while the close stays below the average, and its absence or reversal shows as no fall or a rise.
Forecast: The percent distance of the close from its 200-bar simple moving average, using MovingAverageDistanceComponent with period 200 and average "sma". It is standardised against its own past 200 values, then clipped at a maximum of 0. The forecast is zero while the close is at or above the average. It turns negative (short) once the close is below the average, and the short grows with the distance below, up to -20.
Config: 002-04_price-cross-below-sma-down_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Regress BTC's 24-bar forward return on the forecast. The forward return is taken in excess of the mean 24-bar forward return of all bars in the same window, so the market's own drift is removed. Use non-overlapping 24-bar blocks (or Newey-West with 24 lags) and report the t-stat of the slope; a positive slope means deeper shorts precede larger falls.
- Supporting check: Among bars with forecast < 0, the share followed by a negative 24-bar excess return, compared with 50%.
- Confirm: Slope t ≥ 2 across the pooled windows, and the short-bar fall share is above 50%.
- Reject: Slope t ≤ -2, meaning price rises after the close sits below the average (reversal or exhaustion). A slope near zero does not count as a reject.
- Inconclusive: A slope t between -2 and 2, or a confirm-level slope where the fall share is not above 50%. Also inconclusive if fewer than 200 non-overlapping 24-bar blocks have forecast < 0.
