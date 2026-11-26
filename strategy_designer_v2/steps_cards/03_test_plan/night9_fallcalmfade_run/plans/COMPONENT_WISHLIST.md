# Component wish list

One block per idea that needs components the catalogue does not have.

## 070-01.b1.b1_calm-decline-depth-fade_1d
- Component: PriorDownRunLossOnUpClose: on a bar with close[t] > close[t-1], the fall (close[t-1-n] - close[t-1]) / close[t-1-n] x 100. Here n is the number of consecutive down closes ending at bar t-1, optionally divided by the mean absolute one-bar return over a window. It is 0 on down or flat bars and after no down run, and grows with the depth of the run's total fall. | measures: comparison

## 074-01.b1_falling-deep-run-break-fade_1d
- Component: PriorDownRunLossInUsualMoves: on bar t with close[t] > close[t-1], with n the number of consecutive down closes ending at bar t-1 (capped at `max_bars`), outputs (close[t-1-n] - close[t-1]) / close[t-1-n] / s, where s is the std (ddof 1) of the last 30 one-bar close returns; it is 0 when bar t is not an up close or n = 0; reads closes only; it grows as the finished run's fall deepens in usual daily moves | measures: comparison

## 070-01.g1_calm-decline-long-run-break_1d
- Component: DownRunLengthBeyondFirstOnUpCloseComponent: on a bar with close[t] > close[t-1], max(0, n - 1), where n is the number of consecutive down closes ending at t-1 (close[i] < close[i-1]); 0 on every other bar; usable as a graded forecast source, with its scale taken from its values on up-close bars only, so it grows step by step with each further down day in the broken run | measures: comparison

## 074-01.g1_falling-agitated-scaled-run-break-fade_1d
- Component: PriorDownRunLossInUsualMovesComponent: on a bar with close[t] > close[t-1], it outputs (close[t-1-n] − close[t-1]) / close[t-1-n] / m, else 0. n is the number of consecutive down closes ending at bar t-1. m is the coin's usual daily swing: the mean absolute one-bar close return over the last 30 bars, or their standard deviation (ddof 1). It reads closes only, is never negative, and grows as the ended run's total fall gets larger against the usual daily swing | measures: comparison
