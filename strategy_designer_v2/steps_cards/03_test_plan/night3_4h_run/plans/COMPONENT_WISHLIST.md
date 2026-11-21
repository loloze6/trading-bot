# Component wish list

One block per idea that needs components the catalogue does not have.

## 019-03_upward-breakout-quiet-continuation_4h
- Component: StretchToAverageBarRangeRatio: (max(high) - min(low) over bars t-12..t-1) / mean(high - low over the last 180 bars), from high and low; it falls as the stretch narrows (a "compression" form, its inverse, rises as it narrows) | measures: comparison
- Component: NarrowRangeBreakoutComponent: max(0, close[t] - max(high[t-12..t-1])) / close[t] x 100 x (mean(high - low over 180 bars) / (max(high) - min(low) over t-12..t-1)), from close, high and low; 0 with no breakout, and it grows with the breakout's size and with the stretch's narrowness | measures: situation

## 019-04_downward-breakout-quiet-continuation_4h
- Component: StretchRangeToAverageBarRange: (max(high) − min(low) over the `short_period` bars before bar t, bar t excluded) divided by the mean of (high − low) over the last `long_period` bars (12 and 180 here), from the high and low columns; offered as a "compression" form that grows as the stretch gets narrower relative to the usual bar range | measures: comparison
