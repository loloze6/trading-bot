---
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a sharp one-day fall, sized against the 60-day mean absolute daily move -> adapted: "sharp" made graded (fall / 60-day mean absolute move, cubed as a dead zone).
- Comparison: 20-day volatility high relative to its last 100 days -> kept: a regime rule, 20-day volatility above its 100-day mean.
- Outcome: a rebound (rise) over the next day, larger after a larger fall -> kept: the position is held from the fall's close to the next close (1 bar).
- Verdict transfer: yes: the test measures the idea's fall, inside the idea's volatility condition, against the next day's move.
Forecast: The regime rule reads VolatilityRatioToAverage (20-day return std over its 100-day mean). When it is above 1.0, the regime is mean_reversion. Otherwise the regime is unknown, which is null (flat). In mean_reversion, the component is the 1-day percent return (PriceEvolution, period 1). It is standardised over the prior 60 days, which gives 10 x the return / the 60-day mean absolute daily return, capped at ±20. It is then negated, so a fall reads positive, and clipped at 0, so the strategy is long only after falls and flat on up days. Finally, signed_power with exponent 3 and pivot 10 is applied. A fall of half a usual move gives 1.25, one usual move gives 10, and 1.3 usual moves or more reaches the cap of 20. The forecast is zero away from sharp falls and grows with the fall's size.
Config: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, take (forecast / 10) x (close[t+1]/close[t] - 1 minus that coin's mean daily return over all windows). Measure the mean of this across all coins and windows, with its ordinary t. Each bar is one independent case at a 1-bar horizon.
- Supporting check: Among bars with forecast > 0, split by the median forecast. The mean excess next-day return of the top half minus that of the bottom half must be above 0.
- Confirm: The main measure's t is ≥ 2.0, and the supporting difference is above 0.
- Reject: The main measure's t is ≤ -2.0.
- Inconclusive: A t between -2.0 and 2.0 is inconclusive. So is a t ≥ 2 with a top-minus-bottom difference ≤ 0. So is fewer than 30 bars with forecast > 0, pooled across coins and windows.
