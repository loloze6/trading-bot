# Component wish list

One block per idea that needs components the catalogue does not have.

## 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b1_turbulent-weekend-falls-continue_1h
- Component: WeekendToPriorWeekVolatilityRatio: the std (ddof 1) of the last 48 one-bar close returns (bars t-47..t) divided by the std of the 168 one-bar close returns ending 48 bars earlier (bars t-215..t-48), from closes only; it is 1 when the weekend was as volatile as the prior week and grows continuously as the weekend gets more turbulent (a "centred" form, ratio minus 1, would let it be signed) | measures: comparison

## 026-04_thinner-weekend-larger-reversal.d2_thin-weekends-reverse-when-volatile_1h
- Component: VolatilityWeightedThinVolumeReturn: (close[t] / close[t-48] - 1) x mean(volume[t-167 .. t-48]) / mean(volume[t-47 .. t]) x std (ddof 1) of the 720 one-bar returns ending at bar t, from close and volume; signed like the weekend move, and its size grows with the move, with how thin weekend volume is against the five weekdays before it, and with the coin's 30-day hourly volatility (used negated, on the Sunday 23:00 bar, held 48 bars) | measures: situation
