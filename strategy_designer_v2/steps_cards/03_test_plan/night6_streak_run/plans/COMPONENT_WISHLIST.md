# Component wish list

One block per idea that needs components the catalogue does not have.

## 031-01_up-streak-length-reversal_1d
- Component: UpCloseStreakLength: n, the number of consecutive bars ending at t with close[i] > close[i-1] (0 when bar t did not close higher); read from closes only; grows by one with each further up close | measures: situation
- Component: UpCloseStreakLengthRank: n divided by the mean length of the completed up-close streaks whose bars lie in the last 365 bars (or n's percentile among those lengths); read from closes only; 0 when bar t did not close up; grows as the current streak gets longer than the coin's usual streak | measures: comparison
