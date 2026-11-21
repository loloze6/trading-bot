# Component wish list

One block per idea that needs components the catalogue does not have.

## 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d1_late-utc-rebound-after-falls_1h
- Component: VolatilityWeightedFallComponent: max(0, -(close[t] / close[t-24] - 1)) x the standard deviation of the last 168 one-bar returns close[j] / close[j-1] - 1, from closes only; 0 after a 24-hour rise, and it grows with both the depth of the 24-hour fall and the 7-day hourly volatility (24 and 168 as settable periods) | measures: situation
