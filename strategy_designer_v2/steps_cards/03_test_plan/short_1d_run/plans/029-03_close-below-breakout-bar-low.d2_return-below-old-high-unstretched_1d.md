---
idea: 029-03_close-below-breakout-bar-low.d2_return-below-old-high-unstretched
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: close back below the prior 20-day closing high within 10 days of closing above it -> adapted: graded as the close's depth under the old high, from `FailedBreakoutDepthComponent` (period 20, fail_window 10), which uses the most recent breakout in the window.
- Comparison: the smaller the 20-day return into the breakout day, the larger the fall -> replaced: no component gives the 20-day return ending at the breakout bar j, because j moves from bar to bar.
- Outcome: the coin falls over the next 5 days -> kept: short only, horizon 5 bars on daily bars.
- Verdict transfer: no: without the pre-breakout return, the test cannot weight cases toward breakouts with no big rally before them, and that weighting is half of the idea.
Reason: The weighting needs the 20-day return ending at the breakout bar of the current failed breakout, and that bar sits anywhere from 1 to 10 days back. Every return component in the catalogue reads a fixed bar: `PriceEvolutionComponent` reads bar t, and the `lag` of `VolatilityScaledReturnComponent` is a fixed offset. `FailedBreakoutExcursionComponent` measures the push above the old high, not the rally before the breakout. A weighted mean with the current 20-day return is not the same quantity, and it would also hold a position on bars with no failed breakout.
