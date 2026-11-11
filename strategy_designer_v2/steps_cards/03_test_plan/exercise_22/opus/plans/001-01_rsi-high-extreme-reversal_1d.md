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
- Situation: RSI reaches a high extreme -> adapted: "after the extreme" becomes "while the 14-bar RSI is high", and the extreme threshold becomes a graded short side with a cubic dead zone.
- Comparison: behaviour after extreme readings against behaviour after neutral readings -> adapted: neutral readings give a forecast near zero, and the coin's unconditional return is the baseline.
- Outcome: price falls back over the following bars -> kept: the next 5 daily bars' return, short side.
- Verdict transfer: yes: a short sized by how far RSI is above 50, sharpened toward extremes, earns only if high readings are followed by falls beyond the coin's normal drift.
Forecast: The 14-bar RSI pullback on daily bars, (50 − RSI), is standardised against its own past 60 values. A cubic graded dead zone (signed_power exponent 3, pivot 10) keeps the forecast near zero at ordinary readings and makes it large at extremes. A clip at a maximum of 0 keeps only the high-RSI side, so the forecast is never positive. It is zero when RSI is at or below 50, slightly negative when RSI is somewhat above 50, and strongly negative (down to −20) when RSI is at a high extreme. The short position therefore grows with how overbought the coin is.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after bars where the forecast is −10 or lower (the largest shorts), minus the coin's mean 5-bar return over all tested bars. Results are pooled over the 3 coins and 18 windows, before costs, and overlapping 5-bar returns are counted once (non-overlapping blocks).
- Supporting check: The portfolio's before-cost return minus buy-and-hold, per coin; its sign should match the main measure on at least 2 of the 3 coins.
- Confirm: The mean excess 5-bar return after the largest shorts is negative with t ≤ −2 (price falls back relative to its normal drift).
- Reject: The mean excess 5-bar return after the largest shorts is positive with t ≥ +2 (high readings are followed by continuation).
- Inconclusive: Any t between −2 and +2, including estimates near zero or merely of the wrong sign. The test is also inconclusive with fewer than 20 non-overlapping cases where the forecast is −10 or lower.
