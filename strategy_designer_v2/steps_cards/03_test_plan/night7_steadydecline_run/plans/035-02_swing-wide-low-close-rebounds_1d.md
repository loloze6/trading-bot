---
idea: 035-02_swing-wide-low-close-rebounds
brief: 035_wide-day-low-close-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8ae04f0765bb
---
Fidelity:
- Situation: a day's high-to-low range, against the coin's 20-day return swing, with its close near the day's low -> kept: (high − close)/close/s20 is exactly the range in usual moves times the close's nearness to the low.
- Comparison: the coin's daily-return standard deviation over the past 20 days -> kept: s is the 20-bar return std, ddof 1, which includes the current day.
- Outcome: the coin rises over the next day, more for larger readings -> kept: a graded long held for 1 bar.
- Verdict transfer: yes: the forecast is the idea's own product of range multiple and close location, judged on the next day's return.
Forecast: The forecast uses one component, VolatilityScaledDistanceFromHighComponent, set to period 1, source "high", exclude_current 0, base "close" and vol_period 20. Its raw value is (close − high)/close/s20, which is never positive. Negating it gives the day's range in usual 20-day moves times (high − close)/(high − low): the wider the day is against the recent swing, and the nearer the close is to the low, the larger the reading. Standardise (window 60, min_periods 20) scales this against its own past size, so a typical day reads about 10 and the cap is 20. A clip at 0 keeps the forecast long only. It is near 0 when the day closes at its high, and it grows continuously with width and low-close. It is never negative. There is no regime: the idea is a graded relation on every day.
Config: 035-02_swing-wide-low-close-rebounds_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 1 bar
- Main measure: The slope, across all coins and windows, of each bar's next-day return minus the coin's mean daily return (over all its windows), regressed on that bar's forecast. Its t is computed with the bars of one day taken together.
- Supporting check: The mean next-day excess return on bars in the top fifth of forecasts is above the mean on bars in the bottom fifth. The fifths are drawn per coin, so wide low-close days are compared with narrow ones.
- Confirm: The idea is confirmed when the slope is positive with t ≥ 2 and the top-fifth minus bottom-fifth difference is above 0.
- Reject: The idea is rejected when the slope is negative with t ≤ −2, meaning stronger readings are followed by further falls.
- Inconclusive: Any slope with −2 < t < 2 is inconclusive. A positive slope with t ≥ 2 whose top-minus-bottom difference is 0 or below is also inconclusive. The test needs at least 2,000 independent days and at least 500 bars with forecast ≥ 2; with fewer, the result is inconclusive.
