# Component wish list

One block per idea that needs components the catalogue does not have.

## 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d1_late-utc-rebound-after-falls_1h
- Component: VolatilityWeightedFall: the standard deviation of the last 168 one-bar close returns times max(0, -(close[t] / close[t-24] - 1)) x 100, from closes; it is 0 when the coin did not fall over 24 hours and grows with both the volatility and the depth of the fall | measures: situation
