---
idea: 047-03_falling-agitated-scaled-rise-giveback
brief: 047_falling-agitated-two-way-daily-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: a one-day rise in a falling, agitated market -> kept: the falling agitated profile is added by code, and the forecast is non-zero only on up days.
- Comparison: the rise against the standard deviation of daily returns over the past 30 days -> kept: the day's return is divided by the 30-day std of daily returns.
- Outcome: a fall over the next day, larger the larger the scaled rise -> kept: a graded short held for 1 bar.
- Verdict transfer: yes: the forecast is the idea's scaled rise, inside its profile, betting on the next-day fall in proportion.
Forecast: The component is VolatilityScaledReturnComponent with period 1 and vol_period 30. It gives the day's return divided by the std of the last 30 daily returns. It is standardised over its past 60 values (min 20), then negated, then clipped at a maximum of 0. The forecast is 0 on down and flat days. On up days it is negative (short), and its size grows linearly with the rise in usual daily moves. It stays inside the falling agitated profile, which code adds, and is flat elsewhere.
Config: 047-03_falling-agitated-scaled-rise-giveback_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars with forecast below 0. Regress the coin's next-day return, minus its mean daily return over all windows, on abs(forecast). Read the t of the slope, with the cases of one day grouped together.
- Supporting check: On those same bars, the mean of the next-day return minus the coin's mean daily return is below 0.
- Confirm: The slope's t is -2 or less, and the supporting check passes (the mean excess next-day return is below 0).
- Reject: The slope's t is +2 or more: larger scaled rises are followed by larger next-day gains.
- Inconclusive: A slope t between -2 and +2 is inconclusive. So is a slope t of -2 or less when the mean excess next-day return is not below 0. It is also inconclusive with fewer than 100 short bars, or fewer than 60 distinct days.
