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
- Situation: RSI reaches a high extreme -> adapted: a short position that grows with how far RSI(14) sits above 50, steepened so the extremes dominate; "after X" becomes "while X".
- Comparison: extreme readings versus neutral readings -> kept: neutral RSI gives a near-zero position and extremes give the largest positions.
- Outcome: price falls back over the following bars -> kept: short positions gain when price falls next.
- Verdict transfer: yes: a fall after high RSI confirms reversal; a rise or no change rejects it.
Forecast: Take Wilder RSI(14) on daily closes as RSIPullbackComponent (50 − RSI, contrarian). Standardise it against its own past 60 values. Clip at 0 from above so only high RSI (above 50) gives a position, and that position is short. Apply signed_power with exponent 2 and pivot 10, so a mildly high RSI gives a small short and an extreme RSI gives a much larger one. The forecast is 0 when RSI ≤ 50, negative and growing smoothly as RSI rises, never positive.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On bars whose forecast is in the most negative 10% (pooled over coins and windows), compare the coin's next 5-bar return with its average 5-bar return over all bars. Use non-overlapping 5-bar blocks, pooled across BTC, ETH and BNB, before costs.
- Supporting check: Correlation of the forecast with the next 5-bar return, net of the coin's mean, with the same sign in at least 2 of 3 coins.
- Confirm: The next 5-bar return after extreme bars is lower than the unconditional return, with t ≤ −2 on non-overlapping blocks.
- Reject: The next 5-bar return after extreme bars is higher than the unconditional return (continuation), with t ≥ +2.
- Inconclusive: Any t between −2 and +2 is inconclusive, as is any test with fewer than 30 non-overlapping extreme blocks pooled.
