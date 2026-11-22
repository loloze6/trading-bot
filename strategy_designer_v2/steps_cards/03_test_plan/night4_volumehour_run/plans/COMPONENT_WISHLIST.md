# Component wish list

One block per idea that needs components the catalogue does not have.

## 028-01_volume-surge-up-continuation.d2_volume-surge-after-quiet-day_1h
- Component: VolumeShockTimesPriorRiseComponent: max(0, (close[t]/close[t-1]-1)/s) x volume[t]/mean(volume over the last 720 bars) x (close[t-1]/close[t-25]-1)/m. Here s is the std of the last 720 one-bar returns, and m is the mean absolute 24-bar return over the last 720 bars, so the prior rise ends at bar t-1. It is 0 on hours that are not up, signed like the prior 24-hour return, and grows with the size of the shock and of the prior rise | measures: comparison
