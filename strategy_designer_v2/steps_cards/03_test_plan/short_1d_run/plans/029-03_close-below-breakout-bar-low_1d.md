---
idea: 029-03_close-below-breakout-bar-low
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 1063cd22d7e7
---
Fidelity:
- Situation: a failed breakout above the prior 20-day high, ending with a daily close below the breakout day's low -> replaced: no component locates the breakout day and reads its low; the nearest ones (prior-N-bar low, swing lows) are other levels.
- Comparison: how far that close sits below the breakout day's low -> replaced: only distances below window lows or swing lows exist, not below the breakout bar's low.
- Outcome: the coin falls over the next 5 days, more after a deeper close -> kept: 5 bars on daily bars, short side graded by depth.
- Verdict transfer: no: a test built on another level would not measure a close below the breakout day's low, so its result would not transfer to the idea.
Reason: The idea's situation needs the low of the most recent bar that closed above its prior 20-day high, and the close's distance below that low. Both come from one coin's own daily bars and could be one graded, short-only component. No catalogue component computes them, alone or combined. BarsSinceHighComponent gives only how recent the high is, and DistanceFromHighComponent and the swing-low components measure from other levels.
