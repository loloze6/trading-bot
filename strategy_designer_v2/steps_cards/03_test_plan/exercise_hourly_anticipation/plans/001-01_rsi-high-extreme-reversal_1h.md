---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a high extreme -> adapted: graded short that grows as RSI(14) rises above 50, with a smooth dead zone so the size is concentrated at extreme readings.
- Comparison: behaviour after extreme readings vs after neutral readings -> kept: the criterion compares the forward returns after the largest positions with those after near-zero forecasts.
- Outcome: price falls back over the following bars -> adapted: "after X" becomes "while X", so the short is held while RSI stays high and shrinks as it falls; the forward return is measured at 24 bars.
- Verdict transfer: yes: the forecast is large exactly at high RSI readings and the criterion checks whether price falls more after those bars than after neutral ones.
Forecast: RSIPullbackComponent with RSI period 14 outputs (50 − RSI), which is negative when RSI is above 50. It is standardised against its past 60 values (target 10, cap 20). Then `clip` with max 0 keeps only the high-RSI (short) side, and `signed_power` with exponent 2 and pivot 10 damps mild readings and amplifies extreme ones. The forecast is 0 when RSI is at or below 50. It goes smoothly negative as RSI rises: about −2.5 at half the usual distance from 50, −10 at the usual distance, and down to the −20 clip at extremes. It is never positive.
Config: 001-01_rsi-high-extreme-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Per coin, take the mean 24-bar forward close-to-close return after "extreme" bars (forecast ≤ −10) minus the mean after "neutral" bars (forecast = 0 with RSI ≤ 55). Use non-overlapping 24-bar blocks, one sample per block, so overlapping returns count once. This removes the coin's own drift, which is the buy-and-hold comparison.
- Supporting check: Across all bars, the rank correlation between the forecast and the next-24-bar return is positive, meaning more negative forecasts are followed by lower returns.
- Confirm: The extreme-minus-neutral difference is negative in all three coins. It must have t ≤ −2 on the non-overlapping blocks in at least two coins, and the pooled difference must be ≤ −0.2%.
- Reject: The pooled difference is ≥ 0, or no coin reaches t ≤ −1. A positive difference with t ≥ 2 in two coins shows continuation, which also rejects the idea.
- Inconclusive: Anything in between, for example negative in all coins but t ≤ −2 in fewer than two, or mixed signs. A coin with fewer than 30 non-overlapping extreme blocks across its 6 windows counts as inconclusive.
