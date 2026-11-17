# Component wish list

One block per idea that needs components the catalogue does not have.

## 010-01_rsi-above-share-continuation_1d
- Component: RSIShareAboveMidline: the share of the last `window` (30) bars on which the Wilder RSI(`period` 14) of the closes was above 50, minus 0.5 so it is signed; it runs from -0.5 (always below) to +0.5 (always above) and grows as more of those bars sit above the midpoint | measures: situation

## 010-02_rsi-below-share-continuation_1d
- Component: RsiTimeBelowMidlineComponent: the share of the last 30 bars (the period can be set) on which the Wilder RSI(14) of the closes was below 50, centred as share minus 0.5 and negated, so it grows more negative as RSI spends more of the window below 50, from closes | measures: situation

## 010-03_rsi-above-streak-continuation_1d
- Component: RsiMidlineAgeComponent: from the closes, takes the Wilder RSI (`period` 14). It outputs +n while RSI has been above 50 for the last n bars including bar t, and -n while it has been at or below 50, with n capped at `max_bars`; the size grows by one for each further day on the same side. | measures: situation

## 010-04_rsi-below-streak-continuation_1d
- Component: RsiMidlineAgeComponent: from closes, the Wilder RSI (`period` 14) on each bar; outputs -n while RSI has been below 50 for the last n bars including bar t, and +n while it has been at or above 50; n is capped at `max_bars`, and the size grows by one each bar the side holds | measures: situation

## 010-05_rsi-above-share-reversal_1d
- Component: RsiTimeAboveMidlineComponent: from closes, compute the Wilder RSI(`rsi_period` 14) on each of the last `window` (30) bars and output the share of those bars with RSI above 50, minus 0.5. Range -0.5 to +0.5; it grows as RSI spends more of the window above 50. | measures: situation

## 010-06_rsi-below-share-reversal_1d
- Component: RsiTimeBelowMidlineComponent: share of the last 30 bars on which the 14-bar Wilder RSI of the closes was below 50, re-centred as share - 0.5 (from -0.5 to +0.5); it grows as more of the window is spent below 50 | measures: situation

## 010-07_rsi-above-streak-reversal_1d
- Component: RsiMidlineAgeComponent: from closes, the Wilder RSI(`period`, 14) on each bar. Its output is +n while RSI has been above 50 for the last n bars (bar t included) and -n while it has been below 50, capped at `max_bars`. It grows by one with each further bar on the same side and restarts at ±1 when RSI crosses 50. | measures: situation

## 010-08_rsi-below-streak-reversal_1d
- Component: RsiSideAgeComponent: from the closes, the Wilder RSI(`period` 14); outputs n, the number of consecutive bars up to bar t on which RSI has been below 50 (or signed: -n below and +n above), capped at `max_bars`; it is 0 or 1 on the first bar of a run and grows by 1 for each further bar RSI stays on the same side | measures: situation
