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
- Situation: the RSI reaches a high extreme on the coin -> adapted: the extreme becomes a graded short that grows as RSI rises above 50, damped near neutral; "after" becomes "while".
- Comparison: behaviour after extreme readings against behaviour after neutral readings (from the brief) -> kept: the position is near zero at neutral RSI, and returns after the largest positions are judged against the coin's ordinary return.
- Outcome: price falls back over the following bars, giving back part of the run -> kept: the short gains only if the price falls after high readings.
- Verdict transfer: yes: the test measures whether price falls after high RSI more than it does on ordinary bars, which is the idea as stated.
Forecast: The forecast uses a 14-bar Wilder RSI on daily closes, read as (50 - RSI). It is standardised against its own past 60 values, then cubed around pivot 10. This is the strongest graded dead zone, so readings near 50 give almost no position. Finally it is clipped at a maximum of 0, so the forecast is short only. It is zero while RSI is at or below 50. It is slightly negative when RSI is a little above 50. It becomes strongly negative, down to the -20 cap, as RSI climbs to the high values that are unusual for that coin.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take the bars where the forecast is -10 or lower, meaning the largest shorts. For each, measure the coin's 5-bar forward return minus that coin's mean 5-bar return over all bars of the same window. Pool the cases across coins and windows, keep only non-overlapping 5-bar periods, and judge before costs.
- Supporting check: The idea's portfolio return minus the coin's buy-and-hold return, summed over all windows; it should be positive when the main measure confirms.
- Confirm: The mean excess 5-bar return after the largest shorts is negative with t ≤ -2, counting non-overlapping cases.
- Reject: The mean excess 5-bar return after the largest shorts is positive with t ≥ +2, meaning price continues upward rather than reverting.
- Inconclusive: Any t between -2 and +2, including results near zero, is inconclusive. Fewer than 30 non-overlapping cases is also inconclusive.
