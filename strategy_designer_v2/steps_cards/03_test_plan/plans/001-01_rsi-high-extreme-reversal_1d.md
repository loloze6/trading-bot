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
- Situation: RSI reaches a high extreme -> adapted: the extreme becomes graded, with the short sized by how far the 14-bar RSI sits above 50 and damped near 50.
- Comparison: after extreme readings versus after neutral readings -> kept: the criterion compares returns after the largest positions with returns after neutral bars and with the coin's own drift.
- Outcome: price falls back over the following bars -> adapted: "after X" becomes "while X", the holding period is dropped, and the short is held while RSI stays high.
- Verdict transfer: yes: a graded short on high RSI wins exactly when high readings come before falls, and loses or breaks even when they do not.
Forecast: The forecast comes from the 14-bar Wilder RSI on daily closes, taken as 50 − RSI. It is standardised against its own past 60 values, so a typical reading is 10. It is then clipped at 0 from above, so only readings above 50 count and the forecast is never long. A signed_power with exponent 2 and pivot 10 damps readings near 50 and amplifies extreme ones. The forecast is 0 when RSI is 50 or below. It grows more negative, meaning a larger short, the higher RSI rises, reaching a cap of −20 at the most extreme readings. There is no regime: it is active on every bar.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after "extreme" bars, defined as bars with a forecast of −10 or below. From this, subtract the coin's mean 5-bar forward return in the same window (its own drift). Pool across coins and windows, using non-overlapping 5-bar blocks only.
- Supporting check: The rank correlation between the forecast size (|forecast|) and the next 5-bar coin return, over bars with forecast < 0. It should be negative.
- Confirm: The pooled excess forward return after extreme bars is negative with t ≤ −2, and it is negative in at least 2 of the 3 coins.
- Reject: The pooled excess forward return after extreme bars is ≥ 0, or it is negative in fewer than 2 coins with t > −1.
- Inconclusive: A negative pooled excess return with −2 < t ≤ −1, or a significant pooled result with the coins split. The test needs at least 30 non-overlapping extreme blocks pooled and at least 8 per coin; with fewer, the result is inconclusive.
