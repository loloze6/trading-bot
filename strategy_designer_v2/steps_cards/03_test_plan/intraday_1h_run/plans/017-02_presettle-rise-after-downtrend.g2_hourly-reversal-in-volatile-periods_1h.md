---
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: last hour's move, relative to the coin's usual hourly volatility -> kept: the 1-bar return divided by the 24-bar standard deviation of hourly returns.
- Comparison: stronger when the coin's 24-hour volatility is high -> kept: that move is multiplied by the 24-bar volatility over its 720-bar average, which is exactly the component's vol_lookback factor.
- Outcome: over the next hour the coin moves against the last hour's move, and the move is larger for larger scaled moves -> kept: a signed fade sized by the forecast, judged over 1 bar.
- Verdict transfer: yes: the forecast is the idea's scaled, volatility-weighted fade at its own one-hour horizon, so a confirm or a reject carries straight over to the idea.
Forecast: The indicator is VolatilityScaledReturnComponent with period 1, vol_period 24 and vol_lookback 720. It equals the last hour's return divided by the 24-hour volatility, times that volatility over its 30-day average, so it equals the return over the average 24-hour volatility. It is standardised over 500 past values (min_periods 120) and negated. The forecast is short after an up hour and long after a down hour. It is zero only when the hour is flat. Its size grows with the move in usual moves, and more when the current 24-hour volatility is above its usual level. It is capped at ±20. It is ungated and active on every bar.
Config: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On every bar, pooled over coins and windows, compute (postRebalance_current_allocation) x (close[t+1]/close[t] − 1 − the coin's mean hourly return over all its windows). Take the ordinary t of its mean. This is the position's timing gain before costs, against holding the coin.
- Supporting check: Split bars into quintiles of abs(forecast). Compute the mean timing gain per bar in the top quintile minus the bottom quintile. The difference must be above 0, so that gains grow with the size of the position.
- Confirm: The main measure's mean timing gain is positive with t ≥ 2, and the supporting check's top-minus-bottom difference is above 0.
- Reject: The main measure's mean timing gain is negative with t ≤ −2.
- Inconclusive: The idea is neither confirmed nor rejected when t is between −2 and 2. It is also inconclusive when t ≥ 2 but the top-minus-bottom difference is not above 0. At least 10,000 bars with a non-zero position are needed across all coins and windows. Fewer than that is inconclusive.
