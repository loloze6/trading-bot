# Component wish list

One block per idea that needs components the catalogue does not have.

## 016-01_up-grind-price-continuation_1h
- Component: GrindShareOfRise: from the closes over the last 72 bars, R = close[t] / close[t-72] - 1 and T = the sum of the k largest one-bar gains (k = 3); outputs 1 - min(T / R, 1) when R > 0, else 0, so it is 0 at a small or negative rise and grows towards 1 as the rise is carried by many small hourly gains | measures: comparison
