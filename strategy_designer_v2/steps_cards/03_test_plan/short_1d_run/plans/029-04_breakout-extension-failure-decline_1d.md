---
idea: 029-04_breakout-extension-failure-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 1063cd22d7e7
---
Fidelity:
- Situation: a close above the prior 20-day high, a further peak within 3 days, then a close back below the old high, graded by the peak's excursion -> replaced: no catalogue component or combination recovers the old high once the breakout bars enter the window, or the peak excursion above it.
- Comparison: none -> kept
- Outcome: the coin falls over the next 5 days, more after a larger excursion -> kept
- Verdict transfer: no: the situation could only be measured by a different quantity, so the test's verdict would not be the idea's.
Reason: Every catalogue high, such as DistanceFromHigh, BreakoutInMeanRanges or VolatilityScaledDistanceFromHigh, takes its high over a window ending at bar t or t-1. Once the breakout bars fall inside that window, it reads the breakout peak, not the old 20-day high. No lag setting fixes this, and no regime rule supplies it, so neither "closed back below the old high" nor "the peak's excursion above it" can be computed.
