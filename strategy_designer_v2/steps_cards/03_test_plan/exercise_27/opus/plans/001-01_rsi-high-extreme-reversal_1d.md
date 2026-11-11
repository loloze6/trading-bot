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
- Situation: RSI reaches a high extreme on the coin -> adapted: the on/off "extreme" becomes a graded "while RSI is high", with RSI above 50 cubed so only high readings carry weight.
- Comparison: behaviour after extreme readings vs after neutral ones (brief) -> kept: forward returns after the largest positions are compared with the coin's mean return and with flat (neutral) bars.
- Outcome: price falls back over the following bars, giving back part of the run -> kept: short position, judged on the next 5 bars' return.
- Verdict transfer: yes: the short position grows only as RSI rises, so it pays only if price falls after high readings, and it loses if price keeps rising.
Forecast: The forecast uses a 14-bar Wilder RSI, read as (50 - RSI), which is negative when RSI is above 50. This value is standardised against its own last 60 values. A signed power with exponent 3 and pivot 10 is then applied, so moderate readings sit close to 0 and only high RSI gives a sizeable short. The result is clipped at a maximum of 0, so low RSI gives no long. The forecast is 0 when RSI is at or below 50. It turns negative as RSI rises above 50 and grows steeply with the extremity of the reading, down to the -20 cap.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The 5-bar forward close-to-close return after bars in the most negative decile of the forecast, minus the coin's mean 5-bar return over all 24 windows together. Results are pooled over the three coins, using non-overlapping 5-bar returns (or a HAC t-statistic).
- Supporting check: The same excess forward return after those extreme bars, minus the mean 5-bar return after neutral bars (forecast exactly 0). This is computed per coin, to see whether the sign agrees across BTC, ETH and BNB.
- Confirm: The pooled excess forward return after extreme bars is negative, with t ≤ -2. This means price falls relative to holding, so the short positions gain.
- Reject: The pooled excess forward return after extreme bars is positive, with t ≥ +2. This means price keeps rising after high RSI, which is continuation.
- Inconclusive: Any t between -2 and +2, including estimates near zero or slightly on either side. The result is also inconclusive if there are fewer than 30 non-overlapping extreme-decile cases pooled across the three coins.
