---
idea: 043-01_falling-agitated-intraday-drop-rebound
brief: 043_falling-agitated-intraday-selloff-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 0e977cd77240
---
Fidelity:
- Situation: a coin's drop from the day's open to its close, in percent, in a falling, agitated market -> kept: the profile is added by code, and the drop is measured as (open − close) / open x 100 on down days and is 0 on up days.
- Comparison: the larger the drop, the larger the rise -> kept: the position grows with the drop's size.
- Outcome: the price rises over the next day -> kept: long only, held 1 bar.
- Verdict transfer: yes: the test measures the idea's own drop, in its profile, against the next day's return.
Forecast: The forecast uses one indicator, BarBodySizeComponent with form "drop" and relative_to "open". It is the day's open-to-close fall in percent of the open, and it is 0 on days that close at or above their open. It is standardised against its past 60 values, with min_periods 20. The forecast is therefore 0 on up days and positive on down days, about +10 for a usual-sized drop, and it grows in proportion to the drop up to the cap of +20. It is never negative, so the book is long only. Outside the falling-agitated profile, code keeps the book flat.
Config: 043-01_falling-agitated-intraday-drop-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The cases are the in-profile bars with forecast > 0, pooled over coins and windows. Each case's excess return is close[t+1] / close[t] − 1, minus that coin's mean daily return over all its windows. The measure is the least-squares slope of this excess return on the bar's forecast, with its t computed from day-clustered standard errors.
- Supporting check: The forecast-weighted mean excess return of the cases is above 0.
- Confirm: The slope has a t of 2 or more, and the forecast-weighted mean excess return is above 0.
- Reject: The slope has a t of −2 or less.
- Inconclusive: A slope t between −2 and 2 is inconclusive, as is a slope t of 2 or more with a forecast-weighted mean of 0 or below. Fewer than 100 cases, or cases falling on fewer than 50 distinct days, is inconclusive whatever the t.
