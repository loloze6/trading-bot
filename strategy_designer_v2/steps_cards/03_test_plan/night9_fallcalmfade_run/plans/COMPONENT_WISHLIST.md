# Component wish list

One block per idea that needs components the catalogue does not have.

## 074-01.g1_falling-agitated-scaled-run-break-fade_1d
- Component: PriorDownRunLossInUsualMovesComponent: on a bar with close[t] > close[t-1], it outputs (close[t-1-n] − close[t-1]) / close[t-1-n] / m, else 0. n is the number of consecutive down closes ending at bar t-1. m is the coin's usual daily swing: the mean absolute one-bar close return over the last 30 bars, or their standard deviation (ddof 1). It reads closes only, is never negative, and grows as the ended run's total fall gets larger against the usual daily swing | measures: comparison

## 070-01.b1.g1_calm-decline-depth-fade_1d
- Component: PriorDownRunLossInUsualMovesOnUpClose: on a bar with close[t] > close[t-1], (close[t-1-n] − close[t-1]) / close[t-1-n] / m, where n is the number of consecutive down closes ending at t-1 and m is the mean of abs one-bar returns over the 20 bars ending at t-1; 0 on down or flat bars and on up bars not preceded by a down close; from closes only; grows with the run's total fall in usual daily swings | measures: comparison

## 070-01.b1.g2_falling-market-depth-fade_1d
- Component: PriorDownRunLossOnUpCloseInUsualMovesComponent: when close[t] > close[t-1], it reads (close[t-1-n] - close[t-1]) / close[t-1-n] / m, else 0. Here n is the number of consecutive down closes ending at bar t-1, and m is the usual daily swing over the past 20 days (the std or the mean absolute value of the 20 one-bar returns ending at t-1). It reads closes only. It is 0 and up, and grows as the run's summed fall gets larger against that swing. A `lag` 1 setting on `DownStreakLossInUsualMovesComponent` (with `window` 20) would give the same thing | measures: comparison

## 070-01.g1.d1_deep-slide-calm-run-break-fade_1d
- Component: RunBreakDepthComponent: on a bar whose close is above the prior close after n consecutive lower closes, it gives max(0, −(close[t]/close[t−20] − 1) / (s20 × sqrt 20)) × (n − 1 + d), where s20 is the std of the 20 one-bar returns and d is the fraction (close[t−1] − low of the run) / (high of the run − low of the run), a continuous tiebreak. It is 0 on other bars, and it grows continuously with the depth of the 20-day slide in usual moves and with the run's length beyond the first, from closes only | measures: comparison
