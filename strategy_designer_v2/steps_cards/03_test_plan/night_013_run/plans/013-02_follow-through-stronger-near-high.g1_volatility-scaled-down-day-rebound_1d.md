---
idea: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: a coin's fall on a day, scaled by its 20-day volatility -> kept
- Comparison: the fall measured against the coin's own volatility over the previous 20 days -> kept
- Outcome: a rise over the next 1 day, larger after a larger scaled fall -> kept
- Verdict transfer: yes: the forecast is the scaled fall itself, and the test asks whether the next day's excess return grows with it.
Forecast: Today's one-day return divided by the standard deviation of the last 20 one-day returns (VolatilityScaledReturnComponent, period 1, vol_period 20). That is standardised over its past 60 values, then negated so that a fall reads positive, then clipped at 0. The forecast is long only. It is 0 on up days and flat days, where the situation is absent. It is positive on down days and grows in proportion to the depth of the fall in usual moves, up to the cap of 20. It is never short.
Config: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, pooled over all coins and windows, regress the next bar's excess return on the forecast. The excess return is close[t+1]/close[t] - 1 minus that coin's mean daily return over all windows, taken within the same window only. Report the t of the slope.
- Supporting check: The forecast-weighted mean of that next-bar excess return, over bars with forecast > 0, is above 0.
- Confirm: The slope's t is +2 or more and the supporting check passes (forecast-weighted mean excess return above 0).
- Reject: The slope's t is -2 or less: larger scaled falls are followed by smaller next-day returns than holding.
- Inconclusive: A slope t between -2 and +2 is inconclusive. A t of +2 or more with the forecast-weighted mean at or below 0 is also inconclusive. The test needs at least 500 bars with forecast > 0; with fewer, the result is inconclusive.
