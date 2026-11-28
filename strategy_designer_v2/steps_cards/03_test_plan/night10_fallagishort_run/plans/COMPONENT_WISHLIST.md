# Component wish list

One block per idea that needs components the catalogue does not have.

## 048-01_falling-agitated-wide-rise-giveback_1d
- Component: ScaledRiseRangeMultiple: max(0, (close[t]/close[t-1] - 1) / s30) x (high[t] - low[t]) / mean(high[i] - low[i], i = t-29 .. t), where s30 is the std (ddof 1) of the last 30 one-bar returns, read from close, high and low; it is 0 on down and flat days and grows with both the scaled rise and the range multiple (the up-side mirror of `ScaledFallRangeMultipleComponent` with `period` 1, `lag` 0, `window` 30, `scale` "std") | measures: situation
