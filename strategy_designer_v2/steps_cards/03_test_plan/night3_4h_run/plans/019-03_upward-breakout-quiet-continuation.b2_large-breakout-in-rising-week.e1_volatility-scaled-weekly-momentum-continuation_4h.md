---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a coin's 7-day return, in units of its own 4h volatility -> kept: 42-bar return divided by the 20-bar std of 4h returns.
- Comparison: the larger the vol-scaled return, the larger the rise -> kept: the forecast grows with the vol-scaled return.
- Outcome: the coin rises over the next three days -> kept: each bet is held 18 bars and judged on the 18-bar forward return.
- Verdict transfer: yes: the forecast is the idea's own quantity at its own horizon, so a confirm or a reject carries over.
Forecast: One indicator, VolatilityScaledReturnComponent (period 42 = 7 days, vol_period 20, lag 0, vol_lookback 1). It is the 42-bar return divided by the 20-bar std of 4h returns times sqrt(42), standardised over its past 60 values (min 20). The forecast is positive after a week that is strong for the coin's volatility and negative after a weak one. It is 0 only when the return is 0. Its size grows linearly with the vol-scaled return and is capped at ±20. It is signed and has no dead zone, because the idea is a steady relation and not a rare extreme.
Config: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The slope of the coin's 18-bar forward return, minus that coin's mean 18-bar return over all its windows, regressed on the forecast. Sample bars are positions 0, 18, 36, ... of each window, kept inside windows and pooled over coins and windows. Report the t of the slope and the number of cases.
- Supporting check: Split the book's mean daily return before costs into two parts: the gain from the market's own rise and the rest (timing). The timing part must be above 0.
- Confirm: The slope's t is 2 or more over at least 300 non-overlapping cases, and the book's timing gain before costs is above 0.
- Reject: The slope's t is -2 or less over at least 300 non-overlapping cases.
- Inconclusive: Any of these results is inconclusive: - the slope's t is between -2 and 2; - the slope's t is 2 or more but the timing gain is not above 0; - there are fewer than 300 non-overlapping cases.
