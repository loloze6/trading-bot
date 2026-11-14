---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a high extreme on the coin -> adapted: the threshold becomes a graded RSI-above-50 reading, damped near zero away from the extreme, measured "while" rather than "after".
- Comparison: none in the idea; the brief's extreme-versus-neutral contrast is covered by judging against holding the coin -> kept
- Outcome: price falls back over the following bars, giving back part of the run -> adapted: the holding period is dropped, so the short is held only while RSI stays high.
- Verdict transfer: yes: a short sized by how high RSI is profits exactly when price falls after high readings, and loses when it does not.
Forecast: The forecast uses 14-bar Wilder RSI through RSIPullbackComponent, which outputs (50 - RSI) x sf. It is standardised over the 60 previous values, so an average reading is about 10, capped at ±20. It is then clipped at a maximum of 0, so only RSI above 50 counts and the side is short only. Finally signed_power with exponent 3 and pivot 20 applies the strongest graded dead zone. Mild readings sit near zero: a standardised -10 becomes -2.5 and -5 becomes -0.3. The most extreme readings reach -20, a 200% short. The forecast is zero whenever RSI is at or below 50, and the short grows smoothly as RSI rises further above its usual level.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are bars where the forecast is -5 or below, which are the largest shorts. For each case, take the coin's 5-bar forward return minus that coin's mean 5-bar return over all 24 windows together. Use non-overlapping cases only, keeping one case per 5-bar block, with the three coins pooled.
- Supporting check: Mean excess forward return grows more negative as the forecast moves from (-5, -2] to (-10, -5] to ≤ -10.
- Confirm: The mean excess 5-bar return after the largest shorts is negative with t ≤ -2, using non-overlapping cases.
- Reject: The mean excess 5-bar return after the largest shorts is positive with t ≥ +2. That would mean price continues upward after high RSI.
- Inconclusive: Any t between -2 and +2, including results near zero, is inconclusive. It is also inconclusive if there are fewer than 30 non-overlapping cases pooled across the three coins.
