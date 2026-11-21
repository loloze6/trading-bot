---
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ad5059559106
---
Fidelity:
- Situation: the coin's return over the past 7 days, measured against its 30-day volatility -> kept
- Comparison: rises by more than its normal drift -> kept
- Outcome: the coin rises over the next three days, more after a stronger past rise, and falls after a fall -> kept
- Verdict transfer: yes: the forecast is the 7-day volatility-scaled return itself, judged on 3-day returns net of drift, so either result carries over to the idea.
Forecast: The forecast is VolatilityScaledReturnComponent with period 42 (7 days of 4h bars) and vol_period 180 (30 days). Its value is the 42-bar return divided by the 180-bar standard deviation of one-bar returns times sqrt(42). That value is standardised against its own past 181 values (min_periods 45), so it averages about ±10 and is capped at ±20. The forecast is positive after a volatility-scaled rise and negative after a fall. It is near zero when the week was flat, and its size grows in proportion to the scaled move. There is no regime and no dead zone, because the idea is a steady relation.
Config: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Use the non-overlapping 18-bar grid of each window. Per case, take forecast[t]/10 × (close[t+18]/close[t] − 1 − the coin's normal 18-bar drift over all its windows). Measure the mean of this over all coins and windows, with the ordinary t of that mean. Cases are cells with a non-zero forecast.
- Supporting check: On the same cases, the mean unusual move (return minus drift) of the top forecast quintile minus that of the bottom quintile is above 0.
- Confirm: The main mean is positive with t ≥ 2.0 and the quintile difference is above 0.
- Reject: The main mean is negative with t ≤ −2.0.
- Inconclusive: Any t between −2.0 and 2.0 is inconclusive. So is t ≥ 2.0 with a quintile difference at or below 0. At least 500 independent grid cases are needed; with fewer, the result is inconclusive.
