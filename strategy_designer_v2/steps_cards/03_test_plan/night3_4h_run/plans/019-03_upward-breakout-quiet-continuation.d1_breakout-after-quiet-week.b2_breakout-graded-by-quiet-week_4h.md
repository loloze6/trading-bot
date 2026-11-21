---
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 0974d5467d9f
---
Fidelity:
- Situation: a 4h bar closes above the highest high of the prior two days (12 bars) -> kept: a regime rule on `DistanceFromHighComponent` (period 12, source high, exclude_current 1) above 0.
- Comparison: the average 4h range over the past 7 days (42 bars) against the past 60 days (360 bars), quieter giving a larger rise -> replaced: no component computes this ratio alone, and the nearest one also multiplies in the two-day stretch's narrowness, which the idea sets aside.
- Outcome: the coin rises over the next three days (18 bars) -> kept: a long bet held 18 bars.
- Verdict transfer: no: the only available sizing mixes in the narrowness of the stretch, so a result could not be credited to the quiet week.
Reason: Each needed quantity is in a coin's own high and low columns, and a regime plus a graded component could hold the idea. But no component outputs mean(high−low) over 360 bars divided by mean(high−low) over 42 bars. `NarrowRangeBreakoutRangeRatioComponent` contains that ratio only multiplied by B/S, the stretch-narrowness factor. Weighted sums cannot divide that factor out, and no component outputs a mean bar range alone that `standardise` could set against its own past.
