---
idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: the coin's 14-day RSI at the close, by how far it sits above or below 50 -> kept: RSI with period 336 bars (14 days of 1h bars), signed distance from 50 at each close.
- Comparison: the RSI midpoint of 50 -> kept: the sign of RSI minus 50 sets the side, and its size sets the strength.
- Outcome: a higher return over the next 1 to 7 days the further RSI is above 50, and a lower one the further it is below -> kept: the forward return over 7 days (168 bars), the upper end of the stated range, against the coin's average.
- Verdict transfer: yes: the forecast is the signed RSI distance from 50 itself, and the test is whether forward returns rise with it.
Forecast: One component, `RSIPullbackComponent` with period 336, outputs (50 − RSI). It is standardised over its past 337 values (min_periods 84) and then negated, so the forecast equals (RSI − 50) on the scale of its own usual size. The forecast is positive and long when RSI is above 50 and negative and short when RSI is below 50. It is 0 at RSI = 50 and grows linearly with the distance from 50, capped at ±20. It runs on every bar with no regime gate and no dead zone, because the idea is a steady relation. Note: the engine computes the RSI's smoothing over the bar window of about 437 bars, so the 336-bar RSI is slightly influenced by its seed value.
Config: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h_config.json
Criterion:
- Horizon: 168 bars
- Main measure: - Cases are non-overlapping, on bars 0, 168, 336, ... of each window, pooled over coins and windows. - For each case, compute the product of forecast/10 and the coin's 168-bar excess return. The excess return is close[t+168]/close[t] − 1 minus that coin's mean 168-bar return over all its windows. - The measure is the t of the mean of those products, before costs. This tests whether returns above the coin's average grow with the signed size of the forecast.
- Supporting check: The mean product is above 0 in at least 2 of the 3 coins.
- Confirm: The pooled mean product is above 0 with t ≥ 2.0, and the supporting check passes.
- Reject: The pooled mean product is below 0 with t ≤ −2.0, meaning returns run against RSI's side in proportion to its distance from 50.
- Inconclusive: - Any t between −2.0 and 2.0 is inconclusive. - A t ≥ 2.0 with the coin check failing is also inconclusive. - At least 300 non-overlapping cases are required; with fewer, the result is inconclusive.
