# Component wish list

One block per idea that needs components the catalogue does not have.

## 036-02_range-scaled-rally-continuation_1d
- Component: RangeScaledReturnComponent: (close[t] / close[t-`period`] - 1) / mean((high[i] - low[i]) / close[i], i = t-`range_period`+1 .. t), with `period` 3 and `range_period` 30. It reads close, high and low. It is signed like the 3-day return and grows as the rise gets larger against the usual daily range | measures: situation
