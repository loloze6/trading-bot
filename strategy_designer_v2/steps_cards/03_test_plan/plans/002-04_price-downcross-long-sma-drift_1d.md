---
idea: 002-04_price-downcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: price closed below its long average after being above it -> adapted: "after the cross" becomes "while below", graded by the percent distance below the 200-day SMA.
- Comparison: falls more than after random points -> kept: forward returns on short bars are compared with forward returns on all bars of the same windows.
- Outcome: price keeps falling over the following bars -> kept: a short position gains when price falls.
- Verdict transfer: yes: the graded short-while-below forecast holds exactly the bets the idea predicts will pay, and none it does not.
Forecast: The forecast uses one indicator, the percent distance of the close from its 200-day simple moving average. It is standardised over its past 200 values, with a target of 10 and a cap of 20. It is then clipped at a maximum of 0, so it is short only. The forecast is zero while the close is at or above the 200-day SMA. It turns negative as soon as the close drops below the average, starting near 0 at the cross. The short grows smoothly as the close sinks further below the average, up to -20 (a 200% short). It is never positive.
Config: 002-04_price-downcross-long-sma-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The mean 20-bar forward BTC return on bars where the forecast is below 0, minus the mean 20-bar forward return over all bars of the same windows. Bars are sampled every 20 bars so that overlapping returns are counted once, and results are pooled over the 6 windows, before costs.
- Supporting check: Hit rate: the share of short bars followed by a negative 20-bar return, compared with the share of all bars followed by a negative 20-bar return.
- Confirm: The difference is at most -2 percentage points with a t-stat at or below -2. The hit rate on short bars also exceeds the unconditional share by at least 10 points.
- Reject: The difference is 0 or positive, meaning price falls no further after short bars than after random bars. Rejection also follows if the hit rate is not above the unconditional share, or if mean forward returns after the largest-tertile shorts are positive, which would indicate reversal.
- Inconclusive: Any result between the confirm and reject lines is inconclusive. So is any run with fewer than 15 non-overlapping short cases pooled across windows, whatever the numbers show.
