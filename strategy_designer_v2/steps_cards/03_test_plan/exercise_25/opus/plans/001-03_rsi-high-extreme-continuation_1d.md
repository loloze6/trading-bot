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
- Situation: RSI reaches a high extreme -> adapted: RSI above 50, graded and steeply damped below the extreme, held "while" rather than "after".
- Comparison: more rise than after neutral readings -> kept: neutral RSI gives a forecast near zero, so outcomes after large positions are compared with outcomes after neutral bars.
- Outcome: price keeps rising over the following bars -> kept: forward return over a fixed horizon, long side only.
- Verdict transfer: yes: the forecast is largest exactly at high RSI extremes and near zero at neutral readings, so a result on it is a result on the idea.
Forecast: RSI(14) on daily closes, read as momentum (RSI - 50). It is put on the scale of its own last 60 values and clipped at 0, so it is long only and zero when RSI is at or below 50. It then passes through the strongest graded dead zone the guide allows (cubic, pivot 20). Neutral readings stay near zero: a standardised 10 becomes 2.5. The position grows steeply as RSI nears its extreme: a standardised 20 stays 20, which is a 200% long position at the extreme. It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The 5-bar forward close-to-close return after the top 10% of forecast bars, minus the 5-bar forward return after neutral bars (forecast below 1). Both are taken within the same coin and window, so the coin's own drift cancels. The differences are pooled over the 3 coins and 6 windows, counting only non-overlapping 5-bar returns, before costs.
- Supporting check: The sign of that difference, per coin, for BTC, ETH and BNB separately.
- Confirm: The pooled difference is positive with t >= 2, from at least 30 non-overlapping extreme cases.
- Reject: The pooled difference is negative with t <= -2, from at least 30 non-overlapping extreme cases.
- Inconclusive: Any t between -2 and 2, a difference near zero, or fewer than 30 non-overlapping extreme cases.
