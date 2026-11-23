---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.d1_weekend-fall-size-rebound
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin fell from Saturday close to Sunday close, and its Sunday close is below its 50-day average -> kept: a regime rule fires when the coming bar is Monday and the close sits below SMA(50); the forecast is the Sunday bar's fall, clipped at 0 on rises.
- Comparison: the fall is measured against the coin's own recent daily moves -> kept: the one-bar return divided by the 20-day standard deviation of daily returns (the convention).
- Outcome: the price rises over the next 3 days (Monday to Wednesday), more after larger falls -> kept: a graded long position from Sunday's close, held 3 daily bars.
- Verdict transfer: yes: the test bets on exactly this condition, sized by exactly this measure, over exactly this horizon.
Forecast: The forecast is active only on a Sunday bar's close, which the WeekdayComponent detects as the coming bar being Monday (0). It also needs that close to be below its 50-day simple average (MovingAverageDistanceComponent, period 50, below 0). On those bars it is the Sunday bar's return divided by the standard deviation of the last 20 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). That value is standardised over the last 60 bars, negated, and clipped at 0. So it is positive and grows linearly with the weekend fall in usual daily moves, and it is 0 when Sunday rose. On every other bar it is 0. It is never negative.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average.d1_weekend-fall-size-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: A case is a Sunday bar with a forecast above 0. For each case, take the coin's 3-bar return from the case bar's close, minus the coin's mean 3-bar return over all its windows, and multiply it by forecast / 10. The measure is the mean of these products over all cases, with its t.
- Supporting check: Across the cases, the correlation between the forecast and the excess 3-bar return must be above 0.
- Confirm: The idea is confirmed when the mean of the products is above 0 with t ≥ 2, and the correlation is above 0.
- Reject: The idea is rejected when the mean of the products is below 0 with t ≤ -2.
- Inconclusive: Any result with t between -2 and 2 is inconclusive. So is a confirming t whose correlation is not above 0. The test needs at least 100 cases. Cases fall once a week, so they never overlap.
