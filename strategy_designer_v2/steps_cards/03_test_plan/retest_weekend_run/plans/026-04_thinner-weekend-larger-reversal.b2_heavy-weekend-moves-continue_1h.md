---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a Saturday-Sunday move, graded by its size and by weekend volume against the prior five weekdays' mean -> replaced: no component gives the move times the volume ratio.
- Comparison: weekend volume against the mean volume of the preceding five weekdays -> kept: `VolumeRatioComponent` (period 120, exclude_current 48, short_period 48) as a detector rule, at or above 1.
- Outcome: the price continues in the weekend move's direction over the next 48 hours -> kept: one decision bar per week (Sunday 23:00), held 48 bars.
- Verdict transfer: no: without the product, a heavy-volume weekend with a tiny move gets a large position, so the test would not measure "the more so the larger the move and the heavier the volume".
Reason: The forecast must grow with both the weekend's 48-bar move and the weekend-to-weekday volume ratio, with the move's sign. The config combines components only by weighted sums. A sum of the two, split into regimes by the move's sign, jumps at a zero move and sizes up a flat weekend on heavy volume. `ThinVolumeScaledReturnComponent` gives the inverse ratio (thinner volume reads larger). No catalogue component gives this product.
