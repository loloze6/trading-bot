# Component wish list

One block per idea that needs components the catalogue does not have.

## 058-01_calm-range-top-drifts-down_1d
- Component: HighLowRangePositionComponent: 2 x (close[t] − min(low[t-19..t])) / (max(high[t-19..t]) − min(low[t-19..t])) − 1, with params `period` (20) and 0 for a zero range; read from high, low and close; signed and continuous, rising from −1 at the range's low to +1 at its high, so it grows as the close nears the top | measures: situation
