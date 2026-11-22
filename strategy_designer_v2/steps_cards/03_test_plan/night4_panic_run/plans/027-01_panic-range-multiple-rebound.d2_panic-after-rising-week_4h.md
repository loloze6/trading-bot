---
idea: 027-01_panic-range-multiple-rebound.d2_panic-after-rising-week
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 3503e22a3698
---
Fidelity:
- Situation: a 24-hour fall whose high-low range is a large multiple of the 30-day average 24-hour range -> adapted: the fall condition made graded by the fall's depth (ScaledFallRangeMultipleComponent, period 6, lag 0, window 180).
- Comparison: a return above the coin's usual return, and the 7-day return before the panic -> replaced: no component lets a negative 7-day return lower the forecast only while a panic is present.
- Outcome: a higher 14-day (84-bar) return that grows with the range multiple, and falls with the depth of a negative prior 7-day return -> replaced: a weighted sum of the two readings gives a nonzero position when there is no panic.
- Verdict transfer: no: without the panic-times-prior-return interaction, the idea's exception for falling weeks cannot be confirmed or rejected.
Reason: The idea needs the panic reading multiplied by a factor that falls with the depth of a negative prior 7-day return. Weights only add components, and regimes only switch them, so no combination is zero without a panic, graded by the range multiple, and lowered by the depth of the slide. All the data is in the coin's own bars, but no catalogue component computes this product.
