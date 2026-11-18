# Component wish list

One block per idea that needs components the catalogue does not have.

## 006-05_downside-squeeze-break-continuation_1d
- Component: DistanceBelowPriorLow: (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100 from close and low, negative and growing in size as the close falls further below the prior 20-bar low | measures: situation
- Component: PriorRangeCompressionRatio: 1 - (max(high) - min(low) over bars t-20..t-1) / (max(high) - min(low) over bars t-100..t-1) from high and low, 0 to 1, growing as the band before bar t narrows against the 100-bar range | measures: comparison

## 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d
- Component: RangeWidthRatio: (max high − min low over the last 20 bars) / (max high − min low over the last 100 bars), from high and low; 0 to 1, and it grows as the 20-day range widens toward the full 100-day range | measures: comparison
