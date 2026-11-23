---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's Saturday-to-Sunday close-to-close fall -> kept: the Sunday bar's one-bar return, read at its close when the coming bar is Monday, falls only.
- Comparison: the fall in units of the coin's usual daily move over its past 60 days -> kept: return divided by the mean absolute daily return of the last 60 days.
- Outcome: the price rises over the next 3 days (Monday to Wednesday), more after a larger scaled fall -> kept: 3-bar hold from Sunday's close, sized by the scaled fall.
- Verdict transfer: yes: the forecast is exactly the scaled weekend fall, bought at Sunday's close and held over Monday to Wednesday.
Forecast: A regime rule uses WeekdayComponent to activate the strategy only on the bar whose coming bar is Monday, which is the Sunday bar. Every other bar is flat. On that bar the component is MeanAbsScaledReturnComponent (period 1, window 60). It gives the Sunday return divided by the coin's mean absolute daily return over the last 60 days. It is standardised over its own last 60 values (about 10 per usual move), negated so that a fall reads positive, and clipped at 0 so it is long only. The forecast is 0 after a Sunday rise. After a Sunday fall it is positive and grows linearly with the fall's size in usual moves, capped at 20. Each bet is held 3 bars, Monday to Wednesday.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d2_weekend-fall-in-vol-units_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: A case is a Sunday bar (regime mean_reversion) with forecast >= 2. For each case, take the 3-bar return close[t+3]/close[t]-1 minus the coin's normal 3-bar drift, where the drift is the mean over non-overlapping 3-bar stretches of all its windows. Compute the forecast-weighted mean of this excess return over all coins and windows, and its t, using the ordinary t of the mean of forecast-scaled excess returns.
- Supporting check: Across the same cases, the least-squares slope of the excess 3-bar return on the forecast is positive. This checks that the rise grows with the scaled fall.
- Confirm: The weighted mean excess return is above 0 with t >= 2, and the slope is positive.
- Reject: The weighted mean excess return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 with a slope at or below 0 is also inconclusive. At least 200 cases are needed, counting each Sunday once, before costs.
