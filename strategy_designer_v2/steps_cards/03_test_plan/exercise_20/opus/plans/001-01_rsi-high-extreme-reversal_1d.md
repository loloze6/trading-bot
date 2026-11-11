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
- Situation: RSI reaches a high extreme -> adapted: the threshold is made graded, and "after" becomes "while", using RSI(14) above 50 with a strong dead zone.
- Comparison: behaviour after extreme readings versus after neutral readings -> adapted: neutral readings get a position near zero, and returns after the largest positions are compared with the coin's unconditional return.
- Outcome: price falls back over the following bars -> kept: a short position whose gain is measured on the forward return.
- Verdict transfer: yes
Forecast: The forecast starts from RSIPullbackComponent with period 14, which outputs (50 − RSI) and is negative when RSI is above 50. It is standardised against its own past 60 values (min_periods 20), so a typical deviation is about 10. It then goes through signed_power with exponent 3 and pivot 20. That is the strongest graded dead zone allowed: a standardised 10 becomes 2.5, 15 becomes 8.4 and 20 stays 20. Finally it is clipped at max 0, so only the high-RSI side is kept. The forecast is zero whenever RSI is 50 or below. It is near zero for moderately high RSI. It grows smoothly in the short direction as RSI moves toward extremes, reaching −20 (200% short) when RSI's distance above 50 is about twice its recent average deviation. It is never positive.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's forward 5-bar close-to-close return after bars with forecast ≤ −10, minus the coin's mean 5-bar return over the same window. This is the excess over holding the coin, before costs. Pooled over coins and windows, it is counted once per non-overlapping 5-bar block, and its t-statistic is reported.
- Supporting check: The correlation between the forecast and the next 5-bar excess return is positive in at least 2 of the 3 coins. This means larger short positions are followed by larger relative falls.
- Confirm: The mean excess forward return after extreme bars is negative, so the short gains, with t ≤ −2.0.
- Reject: The mean excess forward return after extreme bars is positive, so price continues up, with t ≥ +2.0.
- Inconclusive: Any t between −2.0 and +2.0 is inconclusive, and so is any test with fewer than 30 non-overlapping extreme cases pooled across coins and windows.
