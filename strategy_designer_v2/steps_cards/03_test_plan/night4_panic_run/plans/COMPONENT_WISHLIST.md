# Component wish list

One block per idea that needs components the catalogue does not have.

## 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h
- Component: FallGatedRangeMultipleTimesVolRatio: from high, low and close, it multiplies three things. The first is G, which is 1 when close[t] < close[t-6] and 0 otherwise. The second is the 6-bar high-low range over its mean over the last 180 bars. The third is s42(t) over the mean of s42 over the last 360 bars, where s42 is the standard deviation of the last 42 one-bar returns. It is 0 without a 24-hour fall, and while the fall lasts it grows continuously with the range multiple and with the volatility ratio. | measures: situation

## 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h
- Component: PriorFallGatedPanicComponent: max(0, -(close[t-12]/close[t-552] - 1)) x 100, which is the 90-day fall ending at the stretch's start, times the `ScaledFallRangeMultipleComponent` (period 6, lag 6, window 180) value, computed from close, high and low; it is 0 unless both the prior 90-day return is negative and the stretch fell, and it grows with the depth of the 90-day fall and with the panic's fall and range multiple | measures: comparison

## 027-01_panic-range-multiple-rebound.d2_panic-after-rising-week_4h
- Component: PanicTimesPriorWeekComponent: the ScaledFallRangeMultipleComponent reading (24h fall depth x 24h range over its 30-day mean, from close, high and low, period 6, window 180), times a factor from the 42-bar return ending 6 bars before t, close[t-6]/close[t-48]-1, counted in usual moves. The factor is 1 when that return is 0 or above and shrinks as it gets more negative, turning negative for a deep slide. The output is 0 without a panic, grows with the range multiple and the fall, and falls as the prior week's slide deepens | measures: situation
