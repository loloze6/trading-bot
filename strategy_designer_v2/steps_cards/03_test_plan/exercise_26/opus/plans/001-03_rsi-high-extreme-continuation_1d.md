---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI reaches a high extreme on the coin -> adapted: the threshold becomes graded (RSI above 50, sharply damped), and "after" becomes "while".
- Comparison: more than after neutral readings -> kept: forward returns after the largest positions are compared with those after near-zero (neutral RSI) bars.
- Outcome: price keeps rising over the following bars -> kept: the forward return of the coin over a fixed horizon, upward.
- Verdict transfer: yes: the test measures whether high RSI readings are followed by larger rises than neutral readings, which is the idea itself.
Forecast: The forecast starts from the 14-bar Wilder RSI on daily bars, taken as RSIPullbackComponent's (50 - RSI) value. It is standardised over its past 60 values, then negated, so it is positive when RSI is above 50. It is clipped at 0 because the idea concerns only high readings. Finally signed_power with exponent 3 and pivot 10 is applied, the strongest graded dead zone the guide allows. The forecast is 0 when RSI is at or below 50 and close to 0 for neutral readings (RSI around 50 to 60). It grows steeply as RSI moves into its upper extreme, reaching the cap of 20 around RSI 70 or higher. It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's forward 5-bar return after bars with forecast >= 10 (extreme high RSI), minus its forward 5-bar return after bars with forecast < 1 (neutral or low RSI). Results are pooled over coins and windows, and overlapping 5-bar returns are counted once (non-overlapping samples or an overlap-adjusted t).
- Supporting check: The same difference is computed per coin; its sign should be positive in at least 2 of 3 coins.
- Confirm: The difference is positive with t >= 2, before costs, with at least 30 non-overlapping extreme cases.
- Reject: The difference is negative with t <= -2 (high RSI is followed by weaker moves than neutral readings), with at least 30 non-overlapping extreme cases.
- Inconclusive: Any t between -2 and 2, including a difference near zero, is inconclusive. So is any result with fewer than 30 non-overlapping extreme cases.
