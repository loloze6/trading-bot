---
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: while the 60-day return is positive, a higher 14-day RSI -> kept: a regime on the 60-bar return above 0, with the RSI level grading the position inside it.
- Comparison: more than the coin's usual 10-day move -> kept: the 10-bar return minus the coin's mean 10-bar return over all windows.
- Outcome: the coin rises more over the next 10 days -> kept: the forward return over 10 bars, upward.
- Verdict transfer: yes: the regime, the RSI grading and the 10-bar excess return are each measured as the idea states them.
Forecast: The regime detector computes the 60-bar percent return (PriceEvolutionComponent, period 60). When it is above 0, the bar is `trending`. Every other bar is `unknown`, which is flat (forecast 0). In `trending`, the forecast is the 14-bar RSI read as momentum. RSIPullbackComponent gives (50 − RSI); `standardise` (window 60, min_periods 20) scales it against its own past, and `negate` turns it into RSI − 50. `clip` at min 0 then keeps only the long side. The forecast is 0 when RSI ≤ 50 and grows continuously as RSI rises above 50, up to +20. It is never short, which matches "refuse to short, lean long in proportion to RSI".
Config: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The sample is the non-overlapping 10-bar grid of each window, on bars whose regime is `trending`, pooled over coins. On it, take the OLS slope of the excess 10-bar forward return on the bar's forecast. The excess return is close[t+10]/close[t] − 1, minus that coin's mean 10-bar return over all windows.
- Supporting check: On the same sample, the mean excess 10-bar return of the top third of forecasts must be above 0.
- Confirm: The idea is confirmed only if both hold: - the slope's t is 2 or more, with at least 100 independent cases; - the top-third mean excess return is positive.
- Reject: The slope's t is −2 or less, with at least 100 independent cases.
- Inconclusive: Any of these results neither confirms nor rejects the idea: - the slope's t is between −2 and 2; - the t is 2 or more but the top third's mean excess return is 0 or below; - there are fewer than 100 independent trending-grid cases.
