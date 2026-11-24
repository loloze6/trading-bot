# Component wish list

One block per idea that needs components the catalogue does not have.

## 031-03_up-streak-length-continuation_1d
- Component: UpStreakLengthRankComponent: from closes, n = the number of consecutive bars ending at t with close[i] > close[i-1] (0 if bar t did not close higher). The output is the share of completed up-close streaks in the past 365 bars whose length is <= n, 0 when n = 0. It rises toward 1 as the current streak becomes longer than the coin's usual up streaks. | measures: comparison

## 031-04_down-streak-length-continuation_1d
- Component: DownStreakLengthComponent: n, the number of consecutive bars ending at t with close[i] < close[i-1], 0 when bar t did not close down; reads closes only; grows by one with each further lower close | measures: situation
- Component: DownStreakLengthRelativeComponent: n divided by the mean length of the down-close streaks completed within the past 365 bars (or n's percentile rank among those lengths), 0 when bar t did not close down; reads closes only; grows as the current streak gets longer than the coin's usual down streaks | measures: comparison

## 031-02.b1.d2_rebound-graded-by-turbulence_1d
- Component: VolatilityRatioWeightedScaledFall: max(0, -(close[t]/close[t-1] - 1)) / s60 x s10 / s60 from closes only, where s10 and s60 are the standard deviations (ddof 1) of the last 10 and 60 one-bar returns ending at bar t; 0 on up or flat days, and it grows with the size of the day's fall in usual 60-day moves and with how far recent volatility sits above the 60-day level | measures: comparison

## 031-02.b1.g1_long-up-streaks-keep-rising_1d
- Component: UpCloseStreakLength: n, the number of consecutive bars ending at t with close[i] > close[i-1] (0 when bar t did not close higher, capped at a `max_bars` setting), from closes only; it rises by one for each further higher close | measures: situation
