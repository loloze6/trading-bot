# Component wish list

One block per idea that needs components the catalogue does not have.

## 016-01_up-grind-price-continuation.g2_persistent-hour-of-day-drift_1h
- Component: SameHourMeanReturn: the mean of the one-bar returns close[t+1-24k] / close[t-24k] - 1 for k = 1..`days` (30), which are the past returns of the coming bar's UTC hour, read from closes; signed, larger the stronger that hour's recent drift | measures: situation
