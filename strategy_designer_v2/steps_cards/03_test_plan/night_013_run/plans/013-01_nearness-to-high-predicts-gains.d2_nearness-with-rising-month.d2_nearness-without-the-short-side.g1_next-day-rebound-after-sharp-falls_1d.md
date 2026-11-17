---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's one-day fall, larger is stronger -> kept
- Comparison: against its own 20-day volatility of daily returns -> kept
- Outcome: higher return over the next 1 day, upward -> kept
- Verdict transfer: yes: the forecast is the fall divided by 20-day volatility, and the test checks that next-day return rises with it.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 1 and vol_period 20. Its value is today's return divided by the standard deviation of the last 20 daily returns. That value is standardised over the 60 values before it (min_periods 20). It is then negated and clipped at 0. The forecast is positive only on down days, and it grows in line with the fall measured in usual moves, up to a cap of 20. It is 0 on up days and flat days. It is never short, because the idea makes no claim about up days. The config uses no regime, since the idea holds in any regime.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Use every bar with forecast > 0, pooled over coins and windows; 1-bar samples do not overlap. Regress the next-day excess return on the bar's forecast and take the t of the slope. The excess return is close[t+1]/close[t] − 1, minus that coin's mean daily return over all its windows.
- Supporting check: On the daily book, the mean timing gain must be above 0. The timing gain is the position held times the coin's daily return minus that coin's mean daily return. This checks the effect against simply holding the coin.
- Confirm: The slope t must be 2 or more, and the mean timing gain must be above 0.
- Reject: The slope t is −2 or less.
- Inconclusive: Any slope t between −2 and 2 is inconclusive. So is a slope t of 2 or more with a timing gain of 0 or less. The test needs at least 500 bars with forecast > 0; with fewer, the result is inconclusive.
