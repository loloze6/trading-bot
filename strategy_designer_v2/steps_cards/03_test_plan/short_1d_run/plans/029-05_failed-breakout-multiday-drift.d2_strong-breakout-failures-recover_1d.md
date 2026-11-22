---
idea: 029-05_failed-breakout-multiday-drift.d2_strong-breakout-failures-recover
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: a close back below the old 20-day high within 3 days of a close above it -> adapted: "after X" made "while X", using FailedBreakoutExcursionComponent (period 20, fail_window 4) on closes.
- Comparison: how far the breakout's highest close extended above the old high -> replaced: the catalogue only measures the highest high from the breakout bar, not the highest close.
- Outcome: the coin rises over the following 10 days, more after a larger extension -> kept: a 10-bar horizon on 1d bars, though the brief's short-only side allows only a short bet against it.
- Verdict transfer: no: grading by the highest high instead of the highest close tests a different extension measure, so neither verdict would carry over to the idea.
Reason: The failed breakout itself can be built. But the idea grades it by the highest close since the breakout bar against the old 20-day closing high, and no catalogue component or combination computes that. `FailedBreakoutExcursionComponent` uses the highest high, and `FailedBreakoutDepthComponent` measures the depth below the old high, not the extension above it.
