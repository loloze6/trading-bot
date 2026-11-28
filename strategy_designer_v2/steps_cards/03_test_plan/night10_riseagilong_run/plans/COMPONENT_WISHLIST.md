# Component wish list

One block per idea that needs components the catalogue does not have.

## 087-02_agitated-push-off-low-continues_1d
- Component: VolatilityScaledDistanceFromLowComponent: (close[t] − L) / L / s. L is the lowest close over the last `period` bars (3; bar t included, or bars t-3 .. t-1 with `exclude_current` 1). s is the standard deviation (ddof 1) of the last `vol_period` (30) one-bar returns close[j] / close[j-1] − 1, bar t's included. It is 0 at the low and grows linearly as the close stands more usual daily moves above it. It could be an `extreme` "low" setting of `VolatilityScaledDistanceFromHighComponent` | measures: situation
