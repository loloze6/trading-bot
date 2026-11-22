---
idea: 026-04_thinner-weekend-larger-reversal.d2_thin-weekends-reverse-when-volatile
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 08ec5a873928
---
Fidelity:
- Situation: the coin's Saturday-Sunday move, made more so by high hourly volatility over the preceding 30 days -> replaced: the move is computable, but no component multiplies it by the 30-day volatility level.
- Comparison: weekend volume against volume over the preceding five weekdays, the lower the stronger -> kept: `ThinVolumeScaledReturnComponent` (period 48, volume_period 48, base_near 48, base_far 167) gives the Friday-close-to-Sunday-close move times weekday mean volume over weekend mean volume.
- Outcome: the share of the weekend move reversed over Monday and Tuesday -> kept: a regime active only on the Sunday 23:00 bar sets a bet against the move, held 48 bars.
- Verdict transfer: no: without the volatility factor, the test cannot show that the reversal grows with the coin's 30-day volatility, so neither a confirm nor a reject would answer the idea.
Reason: The idea is a product of three graded factors: the weekend move, the inverse weekend-to-weekday volume ratio and the 30-day hourly volatility. The config's weighted mean can only add components, score_product mode only gates a regime, and no catalogue component multiplies a return by the level of 30-day hourly volatility. `ThinVolumeScaledReturnComponent` divides by the usual move, which is the opposite, and `RecentToPriorVolatilityWeightedReturnComponent` and `VolatilityScaledReturnComponent` use volatility ratios, not the 30-day level. Turning volatility into a regime threshold would replace a graded "the more so" with an on/off gate, which is not an allowed adaptation.
