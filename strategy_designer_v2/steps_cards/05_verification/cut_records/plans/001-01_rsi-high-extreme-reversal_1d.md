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
- Situation: RSI at a high extreme -> adapted: the threshold becomes graded, so the short size grows as RSI(14) rises above 50 and is damped near 50; "after" becomes "while".
- Comparison: extreme readings versus neutral readings -> kept: neutral RSI gives a near-zero position, and the outcome is judged against holding the coin.
- Outcome: price falls back over the following bars -> kept: the short gains only if price falls after high readings.
- Verdict transfer: yes: the forecast is short exactly while RSI is high, largest at extremes, so its forward returns confirm or reject the reversal claim directly.
Forecast: RSIPullbackComponent (period 14, the daily convention) outputs 50 − RSI, which is negative when RSI is above 50. It is standardised over its past 60 values and clipped at a maximum of 0, so the forecast is short only, never long. A signed_power with exponent 2 and pivot 10 damps readings near 50 towards 0 and amplifies high-extreme readings. The forecast is zero when RSI is at or below 50, slightly negative for mildly high RSI, and down to the −20 cap at the highest RSI.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take the bars where the forecast is −10 or lower (the high-extreme readings). Measure the coin's forward 5-bar return after them, minus the mean forward 5-bar return over all bars of the same coin and window (the holding baseline). Pool across coins and windows, and use non-overlapping 5-bar blocks so no return is counted twice.
- Supporting check: The sign of that excess return in each of the 3 coins separately.
- Confirm: The pooled excess forward return is negative with t ≤ −2, and it is negative in at least 2 of the 3 coins.
- Reject: The pooled excess forward return is positive with t ≥ +2 (continuation, not reversal).
- Inconclusive: Any t strictly between −2 and +2, or fewer than 30 non-overlapping extreme cases pooled; the minimum is 30 cases.
