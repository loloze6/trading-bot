# Component wish list

One block per idea that needs components the catalogue does not have.

## 027-01_panic-range-multiple-rebound.d2_panic-after-rising-week_4h
- Component: PanicTimesPriorWeekComponent: the ScaledFallRangeMultipleComponent reading (24h fall depth x 24h range over its 30-day mean, from close, high and low, period 6, window 180), times a factor from the 42-bar return ending 6 bars before t, close[t-6]/close[t-48]-1, counted in usual moves. The factor is 1 when that return is 0 or above and shrinks as it gets more negative, turning negative for a deep slide. The output is 0 without a panic, grows with the range multiple and the fall, and falls as the prior week's slide deepens | measures: situation
