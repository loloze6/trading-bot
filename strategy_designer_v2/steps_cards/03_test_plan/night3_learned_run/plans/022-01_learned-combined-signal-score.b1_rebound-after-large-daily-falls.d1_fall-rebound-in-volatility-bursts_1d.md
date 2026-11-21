---
idea: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls.d1_fall-rebound-in-volatility-bursts
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 1-day fall, large against its 30-day volatility -> adapted: graded fall size in 30-day usual moves, not a threshold.
- Comparison: the more so the higher 7-day volatility stands against 30-day volatility -> replaced: no component multiplies the fall by the 7d/30d volatility ratio; the weighted sum can only add them.
- Outcome: higher return over the next 1 day, long -> kept: 1 bar on daily bars, long.
- Verdict transfer: no: an additive mix or a different volatility ratio would test another idea, not this interaction.
Reason: The idea's forecast is the product of the day's fall in 30-day volatility units and the ratio of 7-day to 30-day volatility. The engine averages components and cannot multiply them. No catalogue component computes this product: VolatilityRankedFallComponent ranks a single volatility, and VolatilityScaledReturnComponent with vol_lookback gives the fall in 7-day units times s7 against its own mean. Both measure a different quantity.
