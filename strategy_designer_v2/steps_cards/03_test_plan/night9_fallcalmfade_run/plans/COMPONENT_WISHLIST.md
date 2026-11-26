# Component wish list

One block per idea that needs components the catalogue does not have.

## 070-01.b1.b1_calm-decline-depth-fade_1d
- Component: PriorDownRunLossOnUpClose: on a bar with close[t] > close[t-1], the fall (close[t-1-n] - close[t-1]) / close[t-1-n] x 100. Here n is the number of consecutive down closes ending at bar t-1, optionally divided by the mean absolute one-bar return over a window. It is 0 on down or flat bars and after no down run, and grows with the depth of the run's total fall. | measures: comparison

## 070-01.g1_calm-decline-long-run-break_1d
- Component: DownRunLengthBeyondFirstOnUpCloseComponent: on a bar with close[t] > close[t-1], max(0, n - 1), where n is the number of consecutive down closes ending at t-1 (close[i] < close[i-1]); 0 on every other bar; usable as a graded forecast source, with its scale taken from its values on up-close bars only, so it grows step by step with each further down day in the broken run | measures: comparison

## 074-01.g1_falling-agitated-scaled-run-break-fade_1d
- Component: PriorDownRunLossInUsualMovesComponent: on a bar with close[t] > close[t-1], it outputs (close[t-1-n] − close[t-1]) / close[t-1-n] / m, else 0. n is the number of consecutive down closes ending at bar t-1. m is the coin's usual daily swing: the mean absolute one-bar close return over the last 30 bars, or their standard deviation (ddof 1). It reads closes only, is never negative, and grows as the ended run's total fall gets larger against the usual daily swing | measures: comparison

## 070-01.b1.g1_calm-decline-depth-fade_1d
- Component: PriorDownRunLossInUsualMovesOnUpClose: on a bar with close[t] > close[t-1], (close[t-1-n] − close[t-1]) / close[t-1-n] / m, where n is the number of consecutive down closes ending at t-1 and m is the mean of abs one-bar returns over the 20 bars ending at t-1; 0 on down or flat bars and on up bars not preceded by a down close; from closes only; grows with the run's total fall in usual daily swings | measures: comparison

## 070-01.b1.g2_falling-market-depth-fade_1d
- Component: PriorDownRunLossOnUpCloseInUsualMovesComponent: when close[t] > close[t-1], it reads (close[t-1-n] - close[t-1]) / close[t-1-n] / m, else 0. Here n is the number of consecutive down closes ending at bar t-1, and m is the usual daily swing over the past 20 days (the std or the mean absolute value of the 20 one-bar returns ending at t-1). It reads closes only. It is 0 and up, and grows as the run's summed fall gets larger against that swing. A `lag` 1 setting on `DownStreakLossInUsualMovesComponent` (with `window` 20) would give the same thing | measures: comparison
