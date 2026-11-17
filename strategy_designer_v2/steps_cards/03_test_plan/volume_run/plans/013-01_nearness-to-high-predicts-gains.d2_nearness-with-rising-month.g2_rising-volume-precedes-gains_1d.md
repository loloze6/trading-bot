---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: traded volume over the past 5 days, relative to its past 30 days -> replaced: no component computes a 5-day volume mean; `VolumeRatioComponent` reads only one bar's volume.
- Comparison: higher ratio against lower ratio, graded across coins' own history -> kept
- Outcome: higher return over the next 7 days, upward -> kept
- Verdict transfer: no: a one-day volume burst is a different quantity from five days of sustained participation, so a verdict on it would not carry to the idea.
Reason: The situation is mean(volume, last 5 bars) / mean(volume, last 30 bars). `VolumeRatioComponent` gives only the current bar's volume over its own `period`-bar mean. The two ratios at periods 5 and 30 would have to be divided, and component weights can only add them. `standardise` must be the only history op, so a 5-bar smoothing cannot follow it. Score-product mode multiplies only inside a regime gate, not into a graded forecast.
