---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: Sunday's daily return in 20-day daily standard deviations -> adapted: VolatilityScaledReturnComponent(1, 20) is read only while the coming bar is Monday.
- Comparison: the reversal is larger on Sundays with higher volume -> replaced: no catalogue component measures volume against its usual level, and the forecast cannot scale one measure by another.
- Outcome: Monday's return goes against Sunday's move, larger for larger moves, over 1 day -> kept: one daily bar, negated sign.
- Verdict transfer: no: without the volume term the test checks only the size-reversal part, so a confirm or reject would not settle the volume claim.
Reason: A Monday-only regime (WeekdayComponent) and a negated, vol-scaled return can carry the reversal. Two things are missing. The catalogue has no graded measure of a bar's volume against its usual volume. Strategy components combine only as a weighted sum, so "reversal larger with higher volume" needs a component that outputs that product.
