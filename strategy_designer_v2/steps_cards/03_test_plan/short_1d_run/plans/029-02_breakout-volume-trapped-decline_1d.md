---
idea: 029-02_breakout-volume-trapped-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 1063cd22d7e7
---
Fidelity:
- Situation: a daily close above the prior 20-day high, then a close back below that high within 3 days -> replaced: no component gives the broken level or whether today's close sits back below it.
- Comparison: the breakout day's volume against its 20-day average volume -> replaced: the catalogue only gives volume ratios ending at the current bar, not at a breakout bar 1 to 3 days back.
- Outcome: the coin falls over the next 5 days, more after heavier breakout volume -> kept: 5 bars on 1d, short only.
- Verdict transfer: no: without the failed-break state and the breakout day's volume ratio, any config would test a different situation.
Reason: The idea needs only the coin's own closes, highs and volumes. A regime veto on a failure gate plus a graded short sized by the breakout-day volume ratio would hold it. No catalogue component computes either part. `BarsSinceHighComponent` dates a new closing high, but nothing gives the level that high broke or whether the close is back below it. `VolumeRatioComponent` cannot be lagged to a breakout bar that sits 1 to 3 days back.
