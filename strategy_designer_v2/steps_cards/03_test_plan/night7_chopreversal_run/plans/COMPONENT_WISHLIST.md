# Component wish list

One block per idea that needs components the catalogue does not have.

## 044-01_agitated-wide-range-fall-rebound_1d
- Component: FallStdScaledRangeMultipleComponent: max(0, -(close[t]/close[t-1] - 1)) / s x (high[t] - low[t]) / mean(high[i] - low[i], i = t-29 .. t). Here s is the standard deviation (ddof 1) of the last 30 one-bar returns close[j]/close[j-1] - 1, bar t's included, and params are `vol_period` 30 and `range_period` 30. It reads close, high and low. It is 0 on up and flat days, and it grows with the fall in usual standard deviations and with the day's range in average ranges | measures: situation
