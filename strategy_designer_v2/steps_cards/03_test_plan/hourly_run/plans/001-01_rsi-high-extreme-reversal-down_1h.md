---
idea: 001-01_rsi-high-extreme-reversal-down
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme after a one-sided run up -> adapted: graded in the 14-bar RSI's distance above 50, with the high extremes amplified; "after" becomes "while".
- Comparison: versus after neutral readings -> adapted: neutral RSI near 50 gives a forecast near 0, so the test compares the largest positions with all bars.
- Outcome: price falls over the following hours -> kept: the forecast is short-only, measured on forward returns over a fixed number of hours.
- Verdict transfer: yes: the forecast only sizes a short bet on high RSI, so the falls after large forecasts versus neutral bars test the idea directly.
Forecast: Use the RSI pullback with period 14, which is (50 - RSI). Standardise it over its past 60 values (minimum 20). Clip it at a maximum of 0, so only RSI above 50 counts and the side is short only. Then apply signed_power with exponent 2 (pivot 10), so readings near 50 shrink towards 0 and extreme highs grow up to the cap. The forecast is 0 when RSI is at or below 50. It is negative when RSI is above 50, and its size grows quadratically with how far RSI sits above its usual distance from 50. It is never positive.
Config: 001-01_rsi-high-extreme-reversal-down_1h_config.json
Criterion:
- Horizon: 12 bars
- Main measure: Take the bars in the top decile of |forecast| (the extreme-high RSI bars). Measure the mean forward 12-bar log return after those bars, minus the mean forward 12-bar return over all bars of the same coin and window (the unconditional drift, which is what holding the coin earns). Pool all coins and windows, and use a t-statistic on non-overlapping 12-bar blocks (or Newey-West with 12 lags).
- Supporting check: Mean forward 12-bar excess return across quintiles of |forecast| (bars with zero forecast as the neutral group). It should fall steadily as |forecast| grows, with the same sign in at least 2 of the 3 coins.
- Confirm: The pooled excess return after extreme bars is negative with t ≤ -2, and it is negative in at least 2 of 3 coins.
- Reject: The pooled excess return after extreme bars is positive with t ≥ +2, meaning continuation rather than give-back.
- Inconclusive: Any pooled t between -2 and +2, or a pooled t ≤ -2 with fewer than 2 coins agreeing. Either case needs at least 30 non-overlapping extreme episodes per coin and at least 100 pooled; with fewer, the test is inconclusive whatever the t.
