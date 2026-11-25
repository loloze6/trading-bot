# Component wish list

One block per idea that needs components the catalogue does not have.

## 058-02_agitated-rise-swing-scaled-giveback_1d
- Component: MovingAverageDistanceInUsualMovesComponent: (close[t] − SMA) / SMA / s, where SMA is the mean of the last `period` (20) closes including bar t, and s is the standard deviation (ddof 1) of the last `vol_period` (20) one-bar returns close[j] / close[j-1] − 1 ending at bar t; reads closes only; signed, 0 at the average, growing as the close stands more usual daily moves above it (negative below it) | measures: situation
