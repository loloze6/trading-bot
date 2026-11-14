---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme -> adapted: the threshold becomes graded, so the short position grows with RSI above 50, and "after X" becomes "while X".
- Comparison: after extreme readings vs after neutral readings -> adapted: the position is near zero at neutral RSI and largest at extremes, and outcomes are judged against all bars.
- Outcome: price falls back over the following bars -> adapted: the holding period is dropped, so the short is held only while RSI stays high.
- Verdict transfer: yes: a graded short sized by how high RSI sits tests directly whether high readings come before declines.
Forecast: The forecast uses 14-bar Wilder RSI through RSIPullbackComponent, whose raw value is (50 - RSI) x 0.4. This is standardised against its own previous 60 values, so an average reading is 10. Then signed_power with exponent 2 and pivot 10 damps readings near neutral and amplifies extremes, without a cliff. Finally clip with max 0 keeps only the short side. The forecast is negative when RSI is above 50 and grows with the square of how far RSI sits above its usual distance from 50. It is zero whenever RSI is at or below 50. It never goes long.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's mean 5-bar forward close-to-close return after bars with forecast <= -10 (strong short), minus its mean 5-bar forward return over all bars of the same windows. Results are pooled across the three coins, keeping at most one case per 5 bars so that overlapping returns count once.
- Supporting check: Mean 5-bar forward return after bars with forecast between -2 and 0 (neutral RSI). Strong-short bars should fall below this, and the extreme-vs-neutral gap should share the main measure's sign.
- Confirm: The pooled difference is -1.0% or lower with t <= -2.0, and it is negative in at least 2 of the 3 coins.
- Reject: The pooled difference is >= 0. A difference of +1.0% or more with t >= 2.0 would also point to continuation.
- Inconclusive: A pooled difference between -1.0% and 0, or a t-stat between -2.0 and 0, or only 1 of 3 coins agreeing. Fewer than 30 non-overlapping strong-short cases pooled is inconclusive whatever the result.
