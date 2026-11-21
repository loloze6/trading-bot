# Component wish list

One block per idea that needs components the catalogue does not have.

## 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
- Component: QuietWeekNarrowRangeBreakoutComponent: from high, low and close, computes NarrowRangeBreakoutComponent(period 12, base_period 180) x (mean(high−low) over the last 360 bars / mean(high−low) over the last 42 bars). It is 0 with no close above the prior 12-bar high, and grows with the breakout's size, the stretch's narrowness and the quietness of the past week | measures: comparison

## 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h
- Component: PullbackInMeanRangesComponent: max(0, H − close[t]) / B, where H = max(high[t-12..t-1]) and B = mean(high[i] − low[i]) over the last 180 bars including bar t, from the high, low and close columns; 0 at or above the prior high, growing linearly as the close sits deeper below it, in mean bar ranges | measures: situation
