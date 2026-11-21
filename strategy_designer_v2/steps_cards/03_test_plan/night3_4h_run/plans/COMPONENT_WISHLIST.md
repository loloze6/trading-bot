# Component wish list

One block per idea that needs components the catalogue does not have.

## 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
- Component: QuietWeekNarrowRangeBreakoutComponent: from high, low and close, computes NarrowRangeBreakoutComponent(period 12, base_period 180) x (mean(high−low) over the last 360 bars / mean(high−low) over the last 42 bars). It is 0 with no close above the prior 12-bar high, and grows with the breakout's size, the stretch's narrowness and the quietness of the past week | measures: comparison

## 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h
- Component: NarrowRangeBreakdownComponent: max(0, L − close[t]) / close[t] x 100 x B / S, from high, low and close, where L = min(low[t-12..t-1]), S = max(high[t-12..t-1]) − L, and B = mean(high − low) over the last 180 bars; 0 at or above the prior low, rising with the depth of the break and with how narrow the stretch is against B (to be negated for the short side) | measures: comparison
