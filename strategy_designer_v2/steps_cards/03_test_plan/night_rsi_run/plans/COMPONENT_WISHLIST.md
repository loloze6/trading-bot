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
