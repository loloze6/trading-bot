# Component wish list

One block per idea that needs components the catalogue does not have.

## 018-02_hourly-breakout-multiday-continuation_1h
- Component: VolScaledBreakAboveHighComponent: max(0, close[t] - max(high[t-480..t-1])) / close[t] divided by the mean of abs(close[i]/close[i-24] - 1) over the last 30 daily steps (720 bars), from the high and close columns; 0 below the prior high, and it grows as the close sits more usual daily moves above it | measures: situation
- Component: MeanAbsDailyReturnComponent: the mean of abs(close[i]/close[i-24] - 1) over the last 720 bars, from closes; never negative, and it grows with the coin's usual daily move size (the divisor the comparison needs) | measures: comparison
