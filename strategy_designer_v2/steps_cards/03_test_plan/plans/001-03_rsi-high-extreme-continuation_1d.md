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
- Situation: RSI reaching a high extreme -> adapted: the extreme threshold becomes a graded long that grows with RSI above 50 and is amplified near the top by signed_power. "After X" becomes "while X".
- Comparison: returns after neutral readings -> kept: neutral RSI (near 50) gives a forecast near 0, and the criterion compares returns after extreme readings with returns after neutral ones.
- Outcome: price keeps rising over the following bars -> kept: forward close-to-close return over the next bars, long side.
- Verdict transfer: yes: higher forward returns after the largest RSI-driven positions than after neutral bars is exactly the idea's claim, and their absence refutes it.
Forecast: The forecast starts from the 14-bar Wilder RSI on daily closes, read as (50 - RSI) by RSIPullbackComponent. Each value is standardised against its own past 60 values (target 10). It is then negated, so it is positive when RSI is above 50, and clipped at 0, so it is long only, as the idea concerns high extremes. Finally it goes through signed_power with exponent 2. The result is 0 when RSI is 50 or below and small when RSI is just above 50. It grows quadratically as RSI moves toward its extreme highs: an RSI around 70 gives roughly 15 to 20 before the 20 cap, and a near-neutral reading gives a few points or less. It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The mean 5-bar forward return of the coin after "extreme" bars minus the mean after "neutral" bars, pooled over 3 coins and 6 windows. Extreme bars are those where the forecast is in its top 20 percent of non-zero values. Neutral bars are those where the forecast is below 1 (RSI near or below 50). Only non-overlapping 5-bar returns are used, each counted once. Results are judged before costs.
- Supporting check: The strategy's portfolio return minus a buy-and-hold of the coin scaled to the strategy's average exposure, per coin, before costs.
- Confirm: The extreme-minus-neutral difference is positive with a t-statistic of at least 2 on non-overlapping samples. It must also be positive in at least 2 of the 3 coins, and the supporting excess must be positive pooled.
- Reject: The pooled difference is zero or negative (t ≤ 0). A t of -2 or below also rejects, and points to reversal instead.
- Inconclusive: A t between 0 and 2, or fewer than 30 non-overlapping extreme cases pooled, or fewer than 30 neutral cases.
