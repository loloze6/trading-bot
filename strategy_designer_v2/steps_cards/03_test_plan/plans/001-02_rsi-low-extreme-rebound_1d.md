---
idea: 001-02_rsi-low-extreme-rebound
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a low extreme -> adapted: graded RSI-14 below 50, damped near 50 and amplified at extremes; "after" becomes "while".
- Comparison: extreme readings against neutral readings -> kept: largest positions are compared with flat (RSI ≥ 50) bars.
- Outcome: price rebounds upward over following bars -> kept: long gains over the next 5 bars, measured against holding the coin.
- Verdict transfer: yes: the forecast is largest exactly when RSI is most oversold, so a rebound shows in its gains and the absence of one shows as none.
Forecast: Uses the 14-bar Wilder RSI on daily closes. The raw value is 50 - RSI when RSI is below 50, and 0 otherwise (long only, because the idea concerns low extremes only). The value is standardised against its own past 60 values (target 10, cap 20). It is then passed through signed_power with exponent 2 and pivot 10. Mild oversold readings shrink smoothly towards 0, and deep oversold readings grow up to the forecast cap of 20. The forecast is zero when RSI is 50 or above, and never negative. Position size rises continuously as RSI falls further.
Config: 001-02_rsi-low-extreme-rebound_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's forward 5-bar return on bars where the forecast is in the top quintile of its positive values (deepest oversold), minus its mean forward 5-bar return on bars where the forecast is 0 (neutral or high RSI). Returns are pooled across coins and windows and taken on non-overlapping 5-bar samples, so overlapping returns count once.
- Supporting check: Rank correlation between the forecast and the forward 5-bar return on bars with a positive forecast. The idea predicts a positive correlation.
- Confirm: The pooled excess return is above 0 with a t-statistic of at least 2 on non-overlapping samples, and it is positive in at least 2 of the 3 coins.
- Reject: The pooled excess return is at or below 0, and it is non-positive in at least 2 of the 3 coins.
- Inconclusive: A positive excess return with a t-statistic below 2, or coins that disagree beyond the rule above. The test also counts as inconclusive with fewer than 30 non-overlapping top-quintile cases pooled, or fewer than 8 for any one coin.
