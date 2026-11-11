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
- Situation: RSI reaches a high extreme -> adapted: graded RSI(14) distance above 50, damped by the strongest graded dead zone, so it is near zero away from the extreme.
- Comparison: extreme readings against neutral readings -> adapted: neutral readings give a position near zero, extreme readings give a large one.
- Outcome: price falls back over the following bars -> kept: the coin's forward return after the largest short positions.
- Verdict transfer: yes: the short position grows only with high RSI readings, so a retracement after them confirms the idea and a continuation rejects it.
Forecast: The forecast starts from the 14-bar Wilder RSI, as (50 - RSI). It is standardised against its own past 60 values, so a typical reading is about 10 and the cap is 20. It is then clipped at a maximum of 0, so only RSI above 50 counts and the position is short only. Last, signed_power with exponent 3 and pivot 20 damps it hard: a standardised -10 becomes -2.5 and -20 stays -20. The forecast is zero when RSI is 50 or lower, close to zero at moderately high RSI, and a large short near the RSI's recent extremes. Its size grows steeply as RSI rises.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward log return after bars with forecast <= -5, minus the coin's mean 5-bar return over the same window (the buy-and-hold drift). Pooled over the 3 coins and 18 windows, with non-overlapping 5-bar blocks counted once.
- Supporting check: The strategy's cumulative return before costs on the active bars is above that of holding the coin over the same bars.
- Confirm: The mean excess forward return after forecast <= -5 is negative, with t <= -2 on non-overlapping cases.
- Reject: The mean excess forward return is positive, with t >= +2 on non-overlapping cases, which means continuation.
- Inconclusive: Any t between -2 and +2 is inconclusive, as is any result with fewer than 30 non-overlapping cases with forecast <= -5.
