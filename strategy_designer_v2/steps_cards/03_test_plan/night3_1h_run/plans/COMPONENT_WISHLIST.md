# Component wish list

One block per idea that needs components the catalogue does not have.

## 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
- Component: DailyDropToMeanAbsDailyReturn: (close[t] / close[t-24] - 1) divided by the mean of abs(close[i] / close[i-24] - 1) over the last 720 bars, from closes; signed, it is more negative the more times the usual daily move the coin fell over the last 24 hours (with a `drop_only` setting giving max(0, -value), which grows with the drop multiple) | measures: situation
