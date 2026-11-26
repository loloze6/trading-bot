# Component wish list

One block per idea that needs components the catalogue does not have.

## 023-01_flat-month-top-falls-back_1d
- Component: HighLowRangePosition: (2 x (close[t] − min(low over the last 30 bars)) / (max(high over the last 30 bars) − min(low over the last 30 bars)) − 1), a continuous signed value from −1 to +1 computed from high, low and close; it grows as the close sits farther above the range middle (0 at the middle, 0 for a zero range) | measures: situation

## 031-03_failed-push-high-traps-buyers_1d
- Component: HighPushAbovePriorHighInMeanRanges: max(0, high[t] − max(high[t-5..t-1])) / mean(high[i] − low[i] over the last 30 bars), from the high and low columns; 0 when the day's high stays at or below the prior 5-day high, and it grows linearly with how far the high pushes above it, in average bar ranges | measures: situation
