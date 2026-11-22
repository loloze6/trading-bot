# Component wish list

One block per idea that needs components the catalogue does not have.

## 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
- Component: WeekendVolatilityWeightedReturn: (close[t] / close[t-48] - 1) x 100 x (std of the 48 one-bar returns ending at bar t / std of the 168 one-bar returns ending at bar t-48), from closes only; signed like the 48-bar move, and its size grows with the fall and with how much more volatile those 48 hours were than the week before them | measures: comparison
