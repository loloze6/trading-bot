---
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin's 5-day return, relative to its own 20-day daily volatility, is large -> kept: the 5-bar return divided by the 20-bar daily return std times sqrt(5), graded, rises only
- Comparison: the return is judged against the coin's own 20-day daily volatility -> kept
- Outcome: the price keeps rising over the next 3 days, more so the larger the scaled rise -> kept: each bet is held 3 bars
- Verdict transfer: yes: the forecast is the idea's own vol-scaled 5-day rise and is held for the idea's 3 days, so a confirm or a reject of the test is a confirm or a reject of the idea.
Forecast: The forecast uses one component, `VolatilityScaledReturnComponent` with period 5, vol_period 20, lag 0 and vol_lookback 1. It is the 5-day return divided by the 20-day std of daily returns times sqrt(5). It is standardised over its past 60 values (min_periods 20), so a typical size is about 10, capped at ±20. It is then clipped at 0, so it is long only, as the idea speaks of rises. The forecast is 0 after a 5-day fall and positive after a rise. It grows in proportion to the rise measured in usual moves. There is no dead zone, because the idea is a steady relation, not a rare extreme.
Config: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping 3-bar grid of each window, all coins pooled. Regress each grid bar's 3-bar forward return, minus the coin's mean 3-bar return over all windows, on that bar's forecast. Report the t of the slope.
- Supporting check: Take the grid bars with forecast > 0. Their mean unusual move (3-bar return minus the coin's normal drift) must be above 0.
- Confirm: Slope t ≥ 2 and the supporting check is positive.
- Reject: Slope t ≤ -2.
- Inconclusive: Any slope t between -2 and 2, or t ≥ 2 with a non-positive supporting check. It is also inconclusive with fewer than 300 grid bars with forecast > 0, or fewer than 1000 grid bars in total.
