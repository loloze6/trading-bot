# Component wish list

One block per idea that needs components the catalogue does not have.

## 029-02_breakout-volume-trapped-decline.d2_failed-breakout-in-calm-volatility_1d
- Component: FailedBreakoutDepthTimesCalmRatio: reads closes only. It is `FailedBreakoutDepthComponent` (`period` 20, `fail_window` 3, `exclude_current` 1) multiplied by s60 / s20. Here s20 is the standard deviation of the last 20 one-bar returns and s60 that of the last 60, both ending at bar t. It is 0 with no failed breakout, and grows as the close sinks under the old high and as the recent 20 days get calmer than the 60. | measures: comparison

## 029-03_close-below-breakout-bar-low.d2_return-below-old-high-unstretched_1d
- Component: FailedBreakoutPriorReturnComponent: for the most recent bar j in t-9..t with close[j] above the highest of close[j-20..j-1], and only while close[t] is below that high, outputs depth(t) x max(0, 1 - R(j)/m) or a similar decreasing weight, where R(j) = close[j]/close[j-20] - 1 and m is the mean absolute 20-bar return; reads closes only; it grows as the close sinks under the old high and as the rally into the breakout shrinks; it is 0 when there is no failed breakout | measures: comparison

## 029-05_failed-breakout-multiday-drift.d2_strong-breakout-failures-recover_1d
- Component: FailedBreakoutCloseExcursionComponent: on closes, with j the most recent bar in t-3..t where close[j] > H(j) and H(j) = max(close[j-20..j-1]), it outputs (max(close[j..t]) − H(j)) / H(j) x 100 when close[t] < H(j), else 0; it grows linearly with how far the breakout's highest close rose above the old high | measures: comparison
