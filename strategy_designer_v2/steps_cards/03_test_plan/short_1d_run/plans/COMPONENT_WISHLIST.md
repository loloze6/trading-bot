# Component wish list

One block per idea that needs components the catalogue does not have.

## 029-01_failed-breakout-depth-decline_1d
- Component: FailedBreakoutDepthComponent: from closes, finds the most recent bar within the last `fail_window` (3) bars whose close beat the highest of its prior `period` (20) closes. It outputs max(0, H_old − close[t]) / H_old x 100, where H_old is that prior 20-close high. The output is 0 when there was no such breakout or the close is still at or above H_old, and it grows linearly as the close sinks deeper below the old high. | measures: situation

## 029-02_breakout-volume-trapped-decline_1d
- Component: FailedBreakoutDepth: for the most recent k in 1..3 with close[t-k] > L_k = max(high[t-k-20 .. t-k-1]), outputs max(0, L_k - close[t]) / L_k x 100 when close[t] < L_k, else 0; reads high and close; grows as the close sinks further back below the broken high | measures: situation
- Component: FailedBreakoutVolumeRatio: for that same failed-breakout bar t-k, outputs volume[t-k] / mean(volume[t-k-19 .. t-k]), and 0 when no breakout of the last 3 bars has failed; reads high, close and volume; grows with the breakout day's volume against its 20-day average | measures: comparison
