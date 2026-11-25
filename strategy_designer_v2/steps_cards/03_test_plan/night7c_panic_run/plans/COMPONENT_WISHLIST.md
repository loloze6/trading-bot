# Component wish list

One block per idea that needs components the catalogue does not have.

## 032-02.b2.d2_graded-monthly-low-rebound_1d
- Component: mean bar range width ratio: mean(high − low) over the last 30 bars divided by mean(high − low) over the last 365 bars, bar t included; never negative, 1 when recent bars are as wide as the past year's, growing as recent daily ranges widen (the reciprocal form of `MeanBarRangeRatioComponent`) | measures: comparison

## 032-02.b2.g1.d1_close-location-on-wide-days_1d
- Component: RangeMultipleWeightedCloseLocation: (2 x (close[t] − low[t]) / (high[t] − low[t]) − 1) x (high[t] − low[t]) / mean(high[i] − low[i], i = t-20 .. t-1), from high, low and close. It is signed, positive in the upper half of the bar, and grows in size as the close nears an extreme and as the day's range widens against the prior 20-day mean; `negate` gives the reversal forecast | measures: situation
