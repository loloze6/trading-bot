# Component wish list

One block per idea that needs components the catalogue does not have.

## 032-02.b1.e1.e1_tight-range-breakouts-continue_1d
- Component: ClosingRangeInUsualMovesComponent: (max(close[t-60..t-1]) − min(close[t-60..t-1])) / close[t-1] / m, where m is the mean of abs(close[j]/close[j-1] − 1) over the last `window` (e.g. 60) one-bar returns. It reads closes only, excludes bar t from the range so the break cannot widen it, and grows as the closing range widens in usual daily moves. A "compression" form (e.g. 1 / (1 + value)) would grow as the range narrows. | measures: comparison

## 032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d
- Component: BreakoutRunUpDiscount: on a bar whose close is above the highest of the prior 60 closes, max(0, 1 − R / m), where R = close[t−1] / close[t−21] − 1 (the 20-day return before the break) and m is the mean absolute 20-day return over the last 120 bars, from closes only; 0 when there is no break; graded, above 0 and growing as the prior run-up shrinks (1 at a flat run-up, above 1 after a prior fall) | measures: comparison
