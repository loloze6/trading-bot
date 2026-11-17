---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a coin's 30-day return is positive, with daily volume high relative to its own 20-day average volume -> replaced: the 30-day condition fits a regime rule, but no catalogue component computes the graded volume ratio.
- Comparison: higher versus lower volume relative to the 20-day average -> replaced: only the on/off VolumeExpansionHedgeComponent and the volume_filter op read volume, and neither is graded.
- Outcome: a higher return over the next 3 days, upward -> kept: 3 bars on daily bars, long, sized by the volume ratio.
- Verdict transfer: no: without a graded relative-volume measure, the test cannot check whether heavier volume brings a higher 3-day return.
Reason: The idea needs a graded measure of today's volume against its own 20-day average. That data is in the coin's own bars, and the config could run it inside a "30-day return positive" regime. No catalogue component outputs it, and no composition can make one: the only volume readers are an on/off component and the volume_filter dead-zone op, which is refused in strategies.
