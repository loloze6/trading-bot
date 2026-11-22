# Component wish list

One block per idea that needs components the catalogue does not have.

## 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b1_turbulent-weekend-falls-continue_1h
- Component: WeekendToPriorWeekVolatilityRatio: the std (ddof 1) of the last 48 one-bar close returns (bars t-47..t) divided by the std of the 168 one-bar close returns ending 48 bars earlier (bars t-215..t-48), from closes only; it is 1 when the weekend was as volatile as the prior week and grows continuously as the weekend gets more turbulent (a "centred" form, ratio minus 1, would let it be signed) | measures: comparison
