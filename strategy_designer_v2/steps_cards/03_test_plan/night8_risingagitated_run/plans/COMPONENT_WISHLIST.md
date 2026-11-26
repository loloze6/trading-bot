# Component wish list

One block per idea that needs components the catalogue does not have.

## 068-02_falling-agitated-run-break-fade_1d
- Component: PriorDownRunOnUpCloseComponent: on a bar with close[t] > close[t-1], the number n of consecutive bars i ending at t-1 with close[i] < close[i-1] (closes only), else 0. Its value grows by one with each further down day in the run before the bounce. It could also be `UpCloseStreakLengthComponent` with a `lag` setting, read on a bar whose up streak is 1. | measures: situation
