---
idea: 046-01_calm-scaled-rise-second-day-continues
brief: 046_calm-large-rise-delayed-follow-through
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 0e977cd77240
---
Fidelity:
- Situation: in a calm market, a one-day rise sized against the coin's 30-day daily swing -> kept: the 30-day volatility-scaled one-day return; zero on falls; the calm condition is added by the profile.
- Comparison: the rise against the standard deviation of the last 30 daily returns -> kept
- Outcome: a larger rise from the close one day after the rise to the close two days after -> kept: a 1-day lag puts the position on from the close of day t+1 to the close of day t+2.
- Verdict transfer: yes: the forecast is the idea's lagged scaled rise, and the gain is the second-day return, so a confirmation or a rejection carries over to the idea.
Forecast: The forecast uses `VolatilityScaledReturnComponent` with period 1, vol_period 30 and lag 1. At each daily close it reads yesterday's one-day return, divided by the standard deviation of the 30 daily returns ending yesterday. It is standardised over its own past 60 values, with min_periods 20, so a typical size is 10, capped at 20. It is then clipped at 0. The forecast is positive the day after an up day and grows linearly with the size of that rise in usual daily moves. It is zero the day after a down day or a flat day, and it is never negative. The position is opened at the close one day after the rise and covers the following day. The market-profile code keeps the book flat outside calm markets.
Config: 046-01_calm-scaled-rise-second-day-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Use only the bars where the forecast is above 0. On those bars, regress the next bar's return, close[t+1]/close[t]-1, minus the coin's mean daily return over all its windows, on the forecast (`post_pipeline_value`). Pool all coins and windows. The measure is the t of the slope, with the cases of one day summed together.
- Supporting check: The forecast-weighted mean of that excess next-bar return, over the same bars, is above 0, so the large calm rises are not given back on the second day.
- Confirm: The slope's t is 2 or more, and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any other result is inconclusive, including a slope with t between -2 and 2, or a confirming slope with a weighted mean at or below 0. The test needs at least 100 bars with a forecast above 0, falling on at least 60 distinct days; fewer is inconclusive.
