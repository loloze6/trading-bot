---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: the coin's last 1-hour return measured against its 24-hour volatility -> kept
- Comparison: the move's size relative to the recent 24-hour volatility -> kept
- Outcome: the next 1-hour return runs opposite to that move, more so the larger the move -> kept
- Verdict transfer: yes: the forecast is the idea's own graded relation (the vol-scaled last-hour return, sign reversed), tested on the next hour against holding the coin.
Forecast: Take the last one-hour return and divide it by the standard deviation of the last 24 one-hour returns. Then put that on its own scale over the previous 60 bars and flip its sign. The forecast is negative (short) after an up hour and positive (long) after a down hour. It is zero only when the hour was flat. Its size grows in proportion to how many usual moves the last hour was, up to the cap of 20. There is no regime; it is active on every bar.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: For each bar, take the coin's next-bar return (close[t+1]/close[t] - 1) minus that coin's mean 1-bar return over all its windows. Regress this on the bar's forecast, pooling all coins and windows, and test whether the slope is above zero. Each bar is a non-overlapping case at h = 1, and returns never cross windows.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive, including a slope near zero. The test needs at least 1,000 bars with a non-zero forecast.
