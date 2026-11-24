# Component wish list

One block per idea that needs components the catalogue does not have.

## 037-01_wide-day-fall-next-day-rebound_1d
- Component: FallTimesRangeMultiple: max(0, −(close[t] / close[t-1] − 1)) × 100 × (high[t] − low[t]) / mean(high[i] − low[i], i = t-14 .. t-1), from close, high and low. It is 0 on up and flat days and grows with the day's percent fall and with the day's range in multiples of its prior 14-day average (the fall-side mirror of `RiseTimesRangeMultipleComponent` with `rise_period` 1, `range_period` 14). | measures: situation
