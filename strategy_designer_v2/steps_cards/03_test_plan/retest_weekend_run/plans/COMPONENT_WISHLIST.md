# Component wish list

One block per idea that needs components the catalogue does not have.

## 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
- Component: VolumeRatioWeightedReturnComponent: the close's return over the last `period` bars (48), divided by the mean absolute `period`-bar return over a `window` (720), times the mean volume of the last `period` bars over the mean volume of the `base_period` bars before them (120, bars t-167 .. t-48), from close and volume. It is signed like the move and grows with the move's size and with the volume ratio, and it is 0 for a flat move | measures: situation
