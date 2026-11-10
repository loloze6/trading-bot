---
idea: 001-04_rsi-low-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a low extreme -> adapted: the extreme threshold is made graded, so the short grows smoothly as RSI(14) falls below 50.
- Comparison: falls after extreme readings versus after neutral readings -> adapted: neutral RSI gives a position near zero, and the test compares outcomes by position size.
- Outcome: price keeps falling over the following bars -> kept: the short gains if price falls.
- Verdict transfer: yes: a short that grows with how low RSI is pays only if declines continue more after low readings than after neutral ones.
Forecast: RSIPullbackComponent, period 14, long_only true, outputs (50 − RSI) when RSI is below 50 and 0 otherwise. It is standardised against its own past 60 values (min 20), then negated, so it is short-only. A signed_power with exponent 2 and pivot 10 then mutes readings near 50 and amplifies deep oversold ones. The forecast is 0 whenever RSI ≥ 50. It is negative when RSI < 50, and the short grows roughly with the square of how far RSI sits below 50, relative to its usual depth. It is never positive.
Config: 001-04_rsi-low-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take non-overlapping 5-bar blocks, pooled over the 3 coins and 6 windows. Compare the coin's forward 5-bar return after bars in the top quintile of |forecast| (deep oversold) with the same return after neutral bars (forecast 0 or in the smallest quintile, RSI near 50). The measure is the difference in mean forward return, before costs; this differencing removes the coin's own drift, which is what holding the coin earns.
- Supporting check: The same difference has the same sign in at least 2 of the 3 coins.
- Confirm: The forward return after extremes minus that after neutral readings is negative with t ≤ −2.
- Reject: The difference is positive with t ≥ +2, meaning reversal rather than continuation.
- Inconclusive: Any t between −2 and +2, or fewer than 30 non-overlapping extreme cases in total.
