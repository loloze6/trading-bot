---
idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal.g1_high-vol-down-day-rebound
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a down day, its fall measured in 20-day volatility, while 20-day volatility is high -> kept: VolatilityScaledReturnComponent (period 1, vol_period 20), negated and clipped at 0, measures the fall; a regime would hold the volatility condition.
- Comparison: 20-day volatility against its own 60-day average -> replaced: the catalogue only gives the 20-day volatility's rank among its last 60 values (VolatilityPercentileRegimeComponent), not its ratio to their mean.
- Outcome: a rise over the next 1 day, larger after larger vol-scaled falls -> kept: a graded long position held 1 bar on daily bars.
- Verdict transfer: no: a rank above the median is not volatility above its 60-day mean, because volatility is right-skewed, so the test would select different bars than the idea.
Reason: The idea's condition is the 20-day volatility divided by the mean of its last 60 values. The config logic could hold this as a regime rule, but no catalogue component computes that ratio. The regime-measure ranks and the volatility-ratio components either rank the volatility or mix it with price-high proximity. Detector rules apply no transforms, and detector components ignore `lookback`, so a 60-bar ratio_to_mean cannot be built there either.
