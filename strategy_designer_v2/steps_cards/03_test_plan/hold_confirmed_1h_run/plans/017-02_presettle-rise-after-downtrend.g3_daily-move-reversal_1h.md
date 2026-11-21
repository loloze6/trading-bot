---
idea: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: a coin's 24-hour return, measured against its usual volatility -> kept
- Comparison: the larger that return is relative to usual volatility, the larger the reversal -> kept
- Outcome: over the next 24 hours, price moves against the 24-hour return -> kept
- Verdict transfer: yes: the forecast is the negated 24-hour volatility-scaled return, and it is judged on the next 24 hours.
Forecast: The base is the coin's 24-bar return divided by its usual hourly volatility times √24. Usual hourly volatility is the standard deviation of the last 168 one-hour returns (one week, a common baseline for hourly realised volatility). This is standardised against its own past 168 values and then negated. The forecast is long after a fall and short after a rise. It is zero when the 24-hour return is zero, and it grows with the size of the move in usual moves, up to ±20. It runs on every bar with no regime.
Config: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use the non-overlapping 24-bar grid of each window, pooled over coins and windows. On it, regress the coin's next-24-bar return minus that coin's mean 24-bar return over all windows on the forecast at bar t. The measure is the slope's t-statistic.
- Supporting check: The book's mean daily timing gain is above 0. The timing gain is the book's daily return before costs minus its gain from the market's own rise.
- Confirm: The slope's t-statistic is 2 or more and the supporting check passes.
- Reject: The slope's t-statistic is -2 or less, meaning larger contrarian positions are followed by worse excess returns.
- Inconclusive: A t-statistic between -2 and 2 is inconclusive. So is a slope t of 2 or more when the timing gain is not above 0. At least 500 independent 24-bar cases are required.
