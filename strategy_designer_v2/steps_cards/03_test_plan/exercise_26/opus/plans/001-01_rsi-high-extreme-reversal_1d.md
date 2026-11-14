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
- Situation: RSI reaches a high extreme -> adapted: the extreme threshold becomes a graded short that grows with how far RSI sits above 50, sharply damped away from the extreme; "after" becomes "while".
- Comparison: behaviour after extreme readings versus after neutral readings (brief) -> kept: neutral RSI gives a forecast near zero, and returns are judged against holding the coin.
- Outcome: price falls back over the following bars, giving back part of the run -> kept: the short pays only if price falls.
- Verdict transfer: yes: the graded short on high RSI makes the same bet as the idea, so its result answers the idea both ways.
Forecast: Take the 14-bar Wilder RSI as (50 - RSI), which is negative when RSI is above 50. Standardise it against its own last 60 values (target 10, cap 20). Clip it at 0 so only the high-RSI short side remains. Then apply signed_power with exponent 3 and pivot 20, the strongest graded dead zone the guide allows. The forecast is 0 when RSI is at or below 50 and close to 0 for moderate readings: a standardised -10 gives -2.5. It grows smoothly to -20, a 200 percent short, as RSI reaches its most extreme highs relative to its recent range. It is never positive.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take each bar where the forecast is -5 or below, the largest shorts. Measure the coin's forward 5-bar return there, minus the mean forward 5-bar return over all bars of the same coin and window (the holding baseline). Pool across coins and windows. Count non-overlapping 5-bar blocks once, or use t-stats corrected for the overlap.
- Supporting check: Compute the same excess return separately for BTC, ETH and BNB, and record its sign for each coin.
- Confirm: The pooled excess forward return after the largest shorts is negative with t ≤ -2, so price falls more than usual after high RSI.
- Reject: The pooled excess is positive with t ≥ +2, so price rises more than usual after high RSI (continuation).
- Inconclusive: Any t between -2 and +2, including excess returns near zero. The test is also inconclusive with fewer than 30 non-overlapping extreme cases pooled.
