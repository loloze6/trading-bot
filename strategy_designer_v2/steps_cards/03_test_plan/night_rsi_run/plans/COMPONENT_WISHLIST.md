# Component wish list

One block per idea that needs components the catalogue does not have.

## 010-05_rsi-above-share-reversal_1d
- Component: RsiTimeAboveMidlineComponent: from closes, compute the Wilder RSI(`rsi_period` 14) on each of the last `window` (30) bars and output the share of those bars with RSI above 50, minus 0.5. Range -0.5 to +0.5; it grows as RSI spends more of the window above 50. | measures: situation

## 010-06_rsi-below-share-reversal_1d
- Component: RsiTimeBelowMidlineComponent: share of the last 30 bars on which the 14-bar Wilder RSI of the closes was below 50, re-centred as share - 0.5 (from -0.5 to +0.5); it grows as more of the window is spent below 50 | measures: situation

## 010-07_rsi-above-streak-reversal_1d
- Component: RsiMidlineAgeComponent: from closes, the Wilder RSI(`period`, 14) on each bar. Its output is +n while RSI has been above 50 for the last n bars (bar t included) and -n while it has been below 50, capped at `max_bars`. It grows by one with each further bar on the same side and restarts at ±1 when RSI crosses 50. | measures: situation

## 010-08_rsi-below-streak-reversal_1d
- Component: RsiSideAgeComponent: from the closes, the Wilder RSI(`period` 14); outputs n, the number of consecutive bars up to bar t on which RSI has been below 50 (or signed: -n below and +n above), capped at `max_bars`; it is 0 or 1 on the first bar of a run and grows by 1 for each further bar RSI stays on the same side | measures: situation
