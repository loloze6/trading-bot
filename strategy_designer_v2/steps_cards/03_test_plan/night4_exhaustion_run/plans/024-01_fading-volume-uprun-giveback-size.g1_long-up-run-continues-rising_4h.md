---
idea: 024-01_fading-volume-uprun-giveback-size.g1_long-up-run-continues-rising
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a coin has just risen for many 4h bars in a row -> adapted: "just risen" becomes "while the run of consecutive up closes lasts", graded by its length.
- Comparison: the run's gain against the coin's typical 4h move over the past 30 days (180 bars) -> replaced: no component measures the gain over the run's own variable length; only fixed-period scaled returns exist.
- Outcome: the price keeps rising over the next three days (18 bars) -> kept.
- Verdict transfer: no: a fixed-period gain does not measure the run's gain, so neither result would transfer to the idea.
Reason: The run's length can be read exactly from `RsiMidlineAgeComponent` with `period` 1, because RSI(1) is above 50 exactly on up-close bars. But that component jumps at the run's end, and no component measures the run's own gain in usual 4h moves. Every gain component (`MeanAbsScaledReturnComponent`, `VolatilityScaledReturnComponent`, `PriceEvolutionComponent`) uses a fixed period. Weighted sums cannot make the period follow the run's length, and `score_product` only gates regimes.
