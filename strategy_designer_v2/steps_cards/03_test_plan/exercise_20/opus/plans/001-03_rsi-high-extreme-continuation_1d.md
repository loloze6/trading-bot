---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme -> adapted: "after RSI reaches a high extreme" made "while RSI is above 50", graded with the strongest dead zone so only high readings carry size.
- Comparison: rise after high readings versus after neutral readings -> kept: forward returns after the largest positions are compared with those after near-flat bars.
- Outcome: price keeps rising over the following bars -> kept: the forward return over a fixed horizon, upward.
- Verdict transfer: yes: an upward excess after high-RSI bars over neutral bars confirms continuation, and a clear shortfall or a proven zero difference rejects it.
Forecast: Wilder RSI(14) on daily closes, as RSIPullbackComponent with long_only false. Its raw value (50 − RSI) is standardised over the past 60 values and then negated, so the reading is positive when RSI is above 50. It is clipped at 0, because the idea concerns high readings only. It then passes through signed_power with exponent 3 and pivot 10. The forecast is therefore 0 when RSI is at or below 50, close to 0 for mildly high RSI, and grows steeply as RSI rises further. A standardised value of 10 gives 10; values at 13 and above hit the cap of 20. The forecast is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The 5-bar forward log return of the coin after bars with forecast ≥ 10 (high-RSI extremes), minus the mean 5-bar forward return after neutral bars (forecast < 1). Both are pooled over coins and windows and use non-overlapping 5-bar blocks. Subtracting the neutral-bar return removes the coin's own drift, which is the buy-and-hold baseline. Costs are ignored. The test is a t-test of the difference.
- Supporting check: The difference has the same sign on at least 2 of the 3 coins.
- Confirm: The difference is positive with t ≥ 2, and the supporting check holds.
- Reject: Either the difference is negative with t ≤ −2 (reversal), or no difference is shown by equivalence: the whole 90% confidence interval of the difference lies inside ±0.5% per 5 bars.
- Inconclusive: Any other result, including t between −2 and 2 with a confidence interval not inside ±0.5%, is neither a confirm nor a reject. At least 30 non-overlapping extreme cases (forecast ≥ 10) are needed in total, or the result is inconclusive.
