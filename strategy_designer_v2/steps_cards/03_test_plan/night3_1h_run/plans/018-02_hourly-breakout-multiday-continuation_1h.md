---
idea: 018-02_hourly-breakout-multiday-continuation
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: the hourly close first rises above its highest price of the prior 20 days -> adapted: "first rises above" is made "while above". The component is positive on each hourly close above the prior 480-bar high (bar excluded), so it fires only at new highs.
- Comparison: the distance above the 20-day high, in multiples of the 30-day average absolute daily return -> kept: it is the break divided by the mean absolute 24-bar return over the last 30 days.
- Outcome: price keeps rising over the next 5 days, more than the coin's usual 5-day return, and more for larger breaks -> kept: the 120-bar return after each case, net of the coin's normal drift, graded by break size.
- Verdict transfer: yes: the component measures this exact break on hourly closes, and the outcome is the idea's own 5-day excess return.
Forecast: One component, VolScaledBreakAboveHighComponent with period 480, step 24 and steps 30. Its raw value is max(0, close − prior 480-bar high of the highs) / close, divided by the mean absolute daily return over the last 30 days. It is standardised over its last 500 values (min_periods 120). The forecast is exactly 0 while the close is at or below the prior 20-day high. It is positive on a breakout, and it grows with how many usual daily moves the close sits above that high, up to the cap of 20. It never goes below zero (long only by construction). The component is already zero away from the breakout, so no extra dead zone is added.
Config: 018-02_hourly-breakout-multiday-continuation_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: The unusual move, measured per case. A case is a long bet (a forecast rise of at least 2 points), read once per 120-bar grid cell of each window. The unusual move is close[t+120]/close[t] − 1 minus the coin's normal 120-bar drift over all its windows. The measure is the mean over cases, with the t of that mean.
- Supporting check: Split the cases at the median of the raw value (`last_history_value` of `break`). The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting check is above 0.
- Reject: The mean unusual move is below 0 with t ≤ −2.
- Inconclusive: Any t between −2 and 2. A t of 2 or more is also inconclusive if the larger-break half does not beat the smaller-break half. At least 30 cases over all coins and windows are needed; with fewer, the test is inconclusive.
