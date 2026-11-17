---
idea: 013-04_heavy-volume-below-high-breakout
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a coin closes above its prior 52-week high -> adapted: a regime on `BarsSinceHighComponent` (lookback 365, max_bars 1) is active only on the breakout bar, so "after the break" becomes "while breaking".
- Comparison: volume over the preceding 10 days relative to its own 90-day average, heavier is larger -> replaced: no component or weighted sum computes the ratio of the 10-day mean volume to the 90-day mean volume.
- Outcome: a larger return over the next 30 days, long -> kept: the 30-day horizon is 30 bars, and the holding period is dropped.
- Verdict transfer: no: without the 10-day over 90-day volume ratio, the graded part of the idea cannot be measured.
Reason: `VolumeRatioComponent` gives only one bar's volume over a period mean. The config combines components only by weighted sums, so it cannot form the ratio mean(volume, 10) / mean(volume, 90), which is VR(90)/VR(10). Standardising VR(10) against its own past values measures a different quantity.
