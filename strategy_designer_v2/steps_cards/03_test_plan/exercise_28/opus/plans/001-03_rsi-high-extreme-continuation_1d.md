---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a high extreme -> adapted: the threshold is made graded, with the position growing as RSI rises above 50 and a cubic dead zone keeping it small away from extremes.
- Comparison: compared with what follows neutral readings -> kept: the forward returns after extreme bars are set against those after bars with RSI near 50, using the logged RSI value.
- Outcome: price keeps rising over the following bars -> adapted: "after the extreme" becomes "while the extreme lasts", and the forward return is judged over a fixed horizon.
- Verdict transfer: yes: the test measures how much the upside move after high RSI exceeds the move after neutral RSI, which is exactly the idea's claim.
Forecast: Use a 14-bar Wilder RSI, read as (50 - RSI). Flip its sign so that RSI above 50 is positive. Standardise it against its own past 60 values. Clip it at 0, so the forecast is zero whenever RSI is at or below 50. Then apply signed_power with exponent 3 and pivot 10. The forecast is near zero for mild readings and grows steeply as RSI moves toward a high extreme. It is never negative, and it is capped at 20.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take the mean 5-bar forward return after extreme bars, meaning forecast ≥ 10. Subtract the mean 5-bar forward return after neutral bars, meaning logged RSI between 45 and 55. Pool BTC, ETH and BNB. Use a t-statistic with Newey-West at 5 lags so that overlapping returns are counted once.
- Supporting check: Compare the mean 5-bar forward return after extreme bars with the coin's mean 5-bar return over all 24 windows pooled (the holding benchmark). The excess should be positive.
- Confirm: The pooled extreme-minus-neutral difference is positive with t ≥ 2, and the supporting check's excess is above 0.
- Reject: The pooled extreme-minus-neutral difference is negative with t ≤ -2, meaning price gives back the move after high extremes.
- Inconclusive: Any t between -2 and 2 is inconclusive, including a difference near zero. A result is also inconclusive with fewer than 30 non-overlapping extreme cases pooled, fewer than 10 per coin, or fewer than 30 non-overlapping neutral cases.
