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
- Situation: RSI reaches a high extreme -> adapted: the threshold becomes graded; the position grows with RSI above 50, cubed so it is near zero away from the extreme.
- Comparison: rise more than after neutral readings -> kept: the criterion compares bars with an extreme forecast against bars with a near-zero (neutral) forecast.
- Outcome: price keeps rising over the following bars -> adapted: "after" becomes "while"; one fixed forward horizon replaces "the following bars".
- Verdict transfer: yes: an RSI(14) extreme on the coin's own closes, followed by up-moves larger than after neutral readings, is exactly what is measured.
Forecast: Uses 14-bar Wilder RSI on daily closes. The raw value is 50 - RSI, negated so that it reads RSI - 50 (momentum). It is standardised against its own last 60 values (average size 10, capped at 20), then clipped at 0 so it is long only when RSI is above 50. Then a cubic graded dead zone with pivot 20 is applied. Results: about 0.3 at a standardised value of 5, 2.5 at 10, 20 at the cap. The forecast is zero when RSI is at or below 50 and near zero for neutral readings. It is large (up to 200% long) only when RSI is at a high extreme for that coin's recent history. It never goes short.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's forward 5-bar return after extreme bars (forecast ≥ 10) minus its forward 5-bar return after neutral bars (forecast < 1). Bars are pooled over BTC, ETH and BNB and all windows. Returns are counted on non-overlapping 5-bar blocks, so overlapping returns count once.
- Supporting check: Compare the portfolio's return per bar with the coin's return times the strategy's average allocation (buy-and-hold at equal exposure). It should be positive in at least 2 of the 3 coins.
- Confirm: The mean extreme-minus-neutral 5-bar return difference is positive with t ≥ 2 on non-overlapping blocks.
- Reject: The mean difference is negative with t ≤ -2, meaning extremes are followed by weaker moves than neutral readings (reversal).
- Inconclusive: Any t between -2 and +2, including a difference near zero. The test also needs at least 30 non-overlapping extreme cases and 30 neutral cases in total; fewer is inconclusive.
