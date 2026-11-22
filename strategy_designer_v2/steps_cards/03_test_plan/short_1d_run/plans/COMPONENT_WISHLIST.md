# Component wish list

One block per idea that needs components the catalogue does not have.

## 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
- Component: FailedBreakoutDepthInUsualMoves: on 1d bars, when the close broke above the prior 20-day closing high 1 to 3 bars ago and close[t] is now back below that old high, it outputs max(0, old high − close[t]) / old high, divided by the standard deviation of the last 20 daily close-to-close returns; otherwise 0. The value grows as the close sinks deeper under the old high and as the 20-day volatility falls. | measures: situation

## 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
- Component: FailedBreakoutVolScaledDepth: max(0, H(j) − close[e]) / H(j) / s(e), with e = t − `lag`. j is the most recent bar in e−`fail_window`+1 .. e with close[j] > H(j), where H(j) is the highest of the `period` closes before j. s(e) is the standard deviation (ddof 1) of the `vol_period` one-bar returns ending at e. The value is 0 when no failed breakout lies in the window, and grows linearly as the re-entry close sinks deeper below the old high in usual daily moves | measures: comparison
