# Component wish list

One block per idea that needs components the catalogue does not have.

## 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
- Component: VolRatioWeightedScaledReturn: (close[t] / close[t-24] - 1) / (s(t) x sqrt(24)) x s(t) / mean(s over the last 720 bars), s being the standard deviation of the last 168 one-bar close returns; signed like the 24-hour move, and its size grows with the move in usual moves and with how far the current 7-day volatility sits above its 30-day mean | measures: comparison
