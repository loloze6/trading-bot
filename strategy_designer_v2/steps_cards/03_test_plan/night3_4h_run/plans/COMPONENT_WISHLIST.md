# Component wish list

One block per idea that needs components the catalogue does not have.

## 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
- Component: BreakoutInMeanRangesComponent: max(0, close[t] − max(high[t-period..t-1])) / mean(high[i] − low[i] over the last base_period bars, bar t included), with period 12 and base_period 180; it reads high, low and close, is 0 at or below the prior high, and grows linearly with the size of the break in average bar ranges | measures: comparison

## 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
- Component: QuietWeekNarrowRangeBreakoutComponent: from high, low and close, computes NarrowRangeBreakoutComponent(period 12, base_period 180) x (mean(high−low) over the last 360 bars / mean(high−low) over the last 42 bars). It is 0 with no close above the prior 12-bar high, and grows with the breakout's size, the stretch's narrowness and the quietness of the past week | measures: comparison
