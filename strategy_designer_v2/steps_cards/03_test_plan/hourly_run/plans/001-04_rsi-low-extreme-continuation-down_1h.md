---
idea: 001-04_rsi-low-extreme-continuation-down
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: hourly RSI at a low extreme after a one-sided run down -> adapted: graded RSI shortfall below 50, squared to stress extremes; "after X" becomes "while X" (RSI itself measures one-sidedness).
- Comparison: returns after extreme readings vs after neutral readings -> kept: the criterion compares returns after the largest positions with returns after zero positions (RSI at or above 50).
- Outcome: price keeps falling over the following hours -> kept: short position, judged on forward coin returns.
- Verdict transfer: yes
Forecast: Uses 14-period RSI on 1h closes, read as (50 - RSI) and clamped at 0 when RSI is 50 or above. This is standardised over its past 60 values and negated, so it signals continuation. It then goes through signed_power (exponent 2, pivot 10) so that moderate readings are damped and extremes are amplified. The forecast is 0 while RSI is at or above 50. It is negative (short) when RSI is below 50, and the short grows smoothly, faster than linearly, as RSI falls toward its low extreme. It is never positive.
Config: 001-04_rsi-low-extreme-continuation-down_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Mean forward 24-bar coin return after bars in the most-short decile of the forecast, minus the mean after zero-forecast bars (RSI ≥ 50). Pooled over coins and windows, with Newey-West t-stat (24 lags) so overlapping returns count once.
- Supporting check: Regression slope of the forward 24-bar return (minus the coin's mean return) on the forecast must be positive, so that larger shorts are followed by larger falls. Uses the same HAC t-stat.
- Confirm: The extreme-minus-neutral difference is negative with t ≤ -2, and it is negative in at least 2 of the 3 coins.
- Reject: The extreme-minus-neutral difference is positive with t ≥ +2, meaning reversal or no extra fall, at matching strength.
- Inconclusive: Any |t| < 2, or coins that split in sign, is inconclusive. A test also needs at least 30 non-overlapping 24-bar extreme episodes per coin and 100 pooled; with fewer it neither confirms nor rejects.
