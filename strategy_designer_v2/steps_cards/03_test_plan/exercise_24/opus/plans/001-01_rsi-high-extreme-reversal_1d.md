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
- Situation: RSI reaches a high extreme -> adapted: the extreme is graded, with the strongest graded dead zone, and "after" becomes "while".
- Comparison: behaviour after extreme readings vs after neutral readings (brief) -> kept: the forecast is near zero at neutral readings, and returns are compared across the two.
- Outcome: price falls back over the following bars, giving back part of the run -> kept: the forward return is short-side, at a fixed horizon.
- Verdict transfer: yes: a significant fall after high-RSI bars, relative to neutral bars, is exactly the idea, and a significant rise is its opposite.
Forecast: Use the 14-bar Wilder RSI as (50 - RSI) x 0.4, which is negative when RSI is above 50. Standardise it over the 60 prior values. Clip it at a maximum of 0, so only the high-RSI side counts and the position is short or flat. Then apply signed_power with exponent 3 and pivot 20, the strongest dead zone allowed. A typical reading (standardised -10) becomes about -2.5, while a reading at twice the usual deviation (-20) stays -20. The forecast is therefore zero whenever RSI is at or below 50. It is near zero for mild readings and grows steeply more negative, meaning a bigger short, as RSI moves further into its high extreme.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's forward 5-bar return after "extreme" bars, where the forecast is -10 or lower. Subtract the mean forward 5-bar return after "neutral" bars, where |forecast| is below 1, on the same coin and window, so the coin's drift is removed. Pool across coins and windows, and count overlapping 5-bar returns once by using non-overlapping blocks.
- Supporting check: Across all bars, the slope of the forward 5-bar return on the forecast should be positive: a more negative forecast should be followed by a more negative return.
- Confirm: The mean excess return after extreme bars is negative, with t ≤ -2.
- Reject: The mean excess return after extreme bars is positive, with t ≥ +2. This would mean high RSI is followed by continuation, not reversal.
- Inconclusive: Any t strictly between -2 and +2 is inconclusive, as is any result with fewer than 20 non-overlapping extreme cases pooled across coins and windows.
