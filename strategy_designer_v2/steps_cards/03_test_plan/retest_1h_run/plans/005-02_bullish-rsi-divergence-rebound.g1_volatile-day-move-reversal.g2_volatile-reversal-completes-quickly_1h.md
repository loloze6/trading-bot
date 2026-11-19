---
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 542c6d25ead4
---
Fidelity:
- Situation: a large one-day move while 20-day volatility is high against its last 100 days -> adapted: "large" is made graded (size grows with the 24-bar move), and "high volatility" is kept as a regime of 480-bar volatility at or above its 2400-bar mean.
- Comparison: the day's move against its 60-day mean absolute daily move -> kept: 24-bar return divided by the mean absolute 24-bar return of the prior 1440 bars.
- Outcome: the price gives back the move, in the opposite direction, within the next 3 days -> adapted: "after the move" becomes "while the move is large", and the 3-day hold is dropped from the config but kept as the 72-bar horizon.
- Verdict transfer: yes: the test fades the measured move, in the stated volatility condition, and judges the result over the stated 3 days.
Forecast: The forecast is active only on bars where the 480-bar (20-day) standard deviation of hourly returns is at or above its mean over the last 2400 bars (100 days). On every other bar it is 0. - It starts from the 24-bar (one-day) percent return. - `standardise` divides that return by the mean absolute 24-bar return over the prior 1440 bars (60 days) and multiplies by 10, capped at ±20. - `negate` turns it into a fade: short after a rise, long after a fall. - `signed_power` (exponent 3, pivot 20) is the strongest graded dead zone. It keeps ordinary days near 0: a move at its 60-day mean size gives about ±2.5. The forecast grows steeply to ±20 for a move twice its mean size or more.
Config: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use the non-overlapping 72-bar grid of each window (positions 0, 72, 144, ...). Take the grid bars in the mean_reversion regime with |forecast| ≥ 10, which is a one-day move of about 1.6 times its 60-day mean size or more. On each such bar, compute sign(forecast) × (close[t+72]/close[t] − 1 − the coin's mean 72-bar return over all windows). Pool these cases across coins and test their mean with the ordinary t.
- Supporting check: Across all grid bars in the regime with forecast ≠ 0, regress the same signed excess return on |forecast|. The slope must be above 0.
- Confirm: The mean signed excess return is positive with t ≥ 2, and the supporting slope is positive.
- Reject: The mean signed excess return is negative with t ≤ −2.
- Inconclusive: Any t between −2 and 2 is inconclusive, as is t ≥ 2 with a slope ≤ 0. Fewer than 30 independent cases pooled, or fewer than 10 on any coin with cases, is also inconclusive.
