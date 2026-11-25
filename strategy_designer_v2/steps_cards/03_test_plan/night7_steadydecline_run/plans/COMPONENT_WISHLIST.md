# Component wish list

One block per idea that needs components the catalogue does not have.

## 039-02_agitated-range-fall-low-close-rebound_1d
- Component: FallInMeanRangesCloseLocationComponent: max(0, close[t-1] − close[t]) / mean(high[i] − low[i], i = t-30 .. t-1) × (high[t] − close[t]) / (high[t] − low[t]) (0.5 when high = low), from close, high and low; 0 on up and flat days, and it grows with the fall counted in average daily ranges and as the close nears the day's low | measures: situation
