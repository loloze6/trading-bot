# Component wish list

One block per idea that needs components the catalogue does not have.

## 026-04_thinner-weekend-larger-reversal_1h
- Component: WeekendThinVolumeReversal: −(close[t]/close[t−48] − 1) / (mean abs 48-bar return over a long window) × (mean volume of bars t−168..t−49 / mean volume of bars t−47..t), from close and volume; signed against the weekend move, it grows with the move's size in usual moves and as weekend volume falls below the prior five weekdays' | measures: situation
- Component: LaggedBaseVolumeRatio: mean volume of the last `short_period` bars over the mean volume of the `period` bars ending `lag` bars before t (here 48 over bars t−168..t−49), from volume; above 0, falling as recent volume thins against the earlier base | measures: comparison

## 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
- Component: WeekendVolatilityWeightedReturn: (close[t] / close[t-48] - 1) x 100 x (std of the 48 one-bar returns ending at bar t / std of the 168 one-bar returns ending at bar t-48), from closes only; signed like the 48-bar move, and its size grows with the fall and with how much more volatile those 48 hours were than the week before them | measures: comparison
