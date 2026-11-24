# Component wish list

One block per idea that needs components the catalogue does not have.

## 031-01.b1.b2_wide-day-extends-strong-run_1d
- Component: RiseTimesRangeMultiple: max(0, close[t]/close[t-5] - 1) x 100 x (high[t] - low[t]) / mean(high[i] - low[i], i = t-19 .. t), from close, high and low; 0 when the 5 days did not rise, and it grows with the rise and with the day's range against its 20-day average | measures: situation
