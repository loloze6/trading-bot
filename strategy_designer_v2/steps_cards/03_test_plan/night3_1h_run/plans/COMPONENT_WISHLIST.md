# Component wish list

One block per idea that needs components the catalogue does not have.

## 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h
- Component: PlungeTimesMonthRiseComponent: max(0, -(close[t]/close[t-24] - 1) / mean over the last 720 bars of abs(close[i]/close[i-24] - 1)) x max(0, close[t]/close[t-720] - 1) x 100, from closes only. It is 0 when there is no 24h fall or when the 30-day return is not positive, and it grows continuously with both the depth of the fall in usual daily moves and the size of the month's rise | measures: comparison
