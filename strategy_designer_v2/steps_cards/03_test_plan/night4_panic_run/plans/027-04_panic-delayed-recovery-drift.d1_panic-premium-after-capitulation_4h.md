---
idea: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 3503e22a3698
---
Fidelity:
- Situation: a 24-hour panic stretch (range several times usual, hard fall) that ended one day ago -> kept: `ScaledFallRangeMultipleComponent` (period 6, lag 6, window 180) reads the 24h fall in usual moves times its range multiple, at one day after the stretch.
- Comparison: the 90-day return before the stretch is deeply negative, and a deeper fall gives a higher return -> replaced: only a regime threshold on an unlagged 90-day return fits, which loses the graded depth and the "before the stretch" window.
- Outcome: the return from 1 to 14 days after the stretch is higher than usual -> kept: held for 78 bars (13 days), starting one day after the stretch.
- Verdict transfer: no: without the graded product of panic size and prior 90-day fall, a result would not show whether the premium grows with the depth of the capitulation.
Reason: The forecast must be the panic reading multiplied by the depth of the 90-day fall that ended where the stretch began. The weighted mean of components cannot multiply two components. A regime rule can only gate on a threshold, and it compares unlagged raw values. No catalogue component computes this product, and no composition in the guide builds it.
