# Component wish list

One block per idea that needs components the catalogue does not have.

## 029-02_breakout-volume-trapped-decline_1d
- Component: FailedBreakoutDepth: for the most recent k in 1..3 with close[t-k] > L_k = max(high[t-k-20 .. t-k-1]), outputs max(0, L_k - close[t]) / L_k x 100 when close[t] < L_k, else 0; reads high and close; grows as the close sinks further back below the broken high | measures: situation
- Component: FailedBreakoutVolumeRatio: for that same failed-breakout bar t-k, outputs volume[t-k] / mean(volume[t-k-19 .. t-k]), and 0 when no breakout of the last 3 bars has failed; reads high, close and volume; grows with the breakout day's volume against its 20-day average | measures: comparison

## 029-03_close-below-breakout-bar-low_1d
- Component: BreakoutBarLowBreakDepth: from high, low and close, finds the most recent bar b within the last `max_bars` bars (b < t) whose close exceeded the highest high of bars b-20 .. b-1, then outputs max(0, (low[b] - close[t]) / low[b] x 100). The value is 0 when there is no such breakout or the close is at or above the breakout bar's low, and it grows continuously as the close sits further below that low. | measures: situation
- Component: BreakoutBarLowBreakDepth (same component): its size is the depth below the breakout day's low that the idea says scales the fall. | measures: comparison

## 029-04_breakout-extension-failure-decline_1d
- Component: failed-breakout excursion: finds a breakout bar b within the last 4 daily bars whose close is above H, where H is the highest close of bars b-20..b-1; takes P, the highest high of bars b..b+3 up to t; outputs (P - H) / H x 100 while close[t] < H, else 0, from close and high, never negative and growing with the size of the failed push above the old high | measures: situation

## 029-05_failed-breakout-multiday-drift_1d
- Component: FailedBreakoutDepthComponent: from closes, with `period` 20, `within` 3 and `lag` 2, and e = t - `lag`, it finds the most recent bar b in e-`within` .. e-1 whose close was above every one of its prior `period` closes. H is the highest close of bars b-`period` .. b-1. The output is max(0, H - close[e]) / H x 100 when such a b exists, else 0. It grows as the failure close sits deeper below the old high; `standardise` then `negate` gives the short forecast | measures: situation
- Component: FailedBreakoutDepthComponent (same component): its graded depth below the old high is the idea's comparison, and its `lag` of 2 starts the hold on day 2, so an 8-bar hold covers days 2 to 10 | measures: comparison
