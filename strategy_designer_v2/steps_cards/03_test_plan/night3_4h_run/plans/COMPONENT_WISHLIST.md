# Component wish list

One block per idea that needs components the catalogue does not have.

## 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
- Component: BreakoutInMeanRangesComponent: max(0, close[t] − max(high[t-period..t-1])) / mean(high[i] − low[i] over the last base_period bars, bar t included), with period 12 and base_period 180; it reads high, low and close, is 0 at or below the prior high, and grows linearly with the size of the break in average bar ranges | measures: comparison
