# Component wish list

One block per idea that needs components the catalogue does not have.

## 048-01_falling-agitated-wide-rise-giveback_1d
- Component: RiseScaledRangeMultiple: max(0, (close[t]/close[t-1] - 1) / s30) x (high[t] - low[t]) / mean(high[i] - low[i], i = t-29 .. t), where s30 is the ddof-1 standard deviation of the last 30 one-bar returns; it reads close, high and low; it is 0 on down or flat days and grows with the rise in usual moves and with the range multiple (the up-side mirror of `ScaledFallRangeMultipleComponent` with `period` 1, `lag` 0, `window` 30, `scale` "std") | measures: situation
