---
idea: 058-03_calm-rise-stretch-continuation
brief: 058_rising-agitated-overextension-gives-back
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a rising, calm market, the close stands above its 20-day average, the further the stronger -> kept: the 20-day SMA distance, long side only, graded; code adds the rising-calm profile.
- Comparison: the close against its 20-day average price -> kept.
- Outcome: the coin rises over the next 5 days, more when the distance is larger -> kept: 5 bars, judged against the coin's normal drift.
- Verdict transfer: yes: the forecast is the idea's distance inside its profile, held for its 5-day horizon, so a confirm or reject of the slope is a confirm or reject of the idea.
Forecast: Inside the rising-calm profile (added by code), the forecast is the percent distance of the close above its 20-day simple moving average. It is standardised against its own past 60 values, so a usual distance gives about +10, capped at +20. It is clipped at 0, so it is long only. It is 0 when the close is at or below the average. It grows continuously the further the close stands above the average. Outside the profile it is 0.
Config: 058-03_calm-rise-stretch-continuation_1d_config.json
Profile: rising calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, on grid bars with forecast > 0. Regress the coin's 5-bar return minus that coin's mean 5-bar return over all windows on the bar's forecast. The measure is the slope's t, with cases on the same day pooled across coins.
- Supporting check: none
- Confirm: The slope is positive with t >= 2: the larger the distance above the average, the larger the rise beyond drift.
- Reject: The slope is negative with t <= -2: a larger distance is followed by a smaller rise, or by a fall.
- Inconclusive: A t between -2 and 2 is inconclusive. Fewer than 100 grid cases with forecast > 0, or fewer than 60 distinct days, is also inconclusive.
