---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 6d77ef5ed57a
---
Fidelity:
- Situation: a coin's Saturday-to-Sunday close-to-close fall, in percent of price -> kept: the Sunday bar's 1-bar percent return, fall side only, on Sunday's close, divided by a near-constant 500-bar mean absolute daily move so the size stays percent-proportional within a coin rather than becoming volatility units.
- Comparison: none; the rise is graded by the depth of the fall -> kept: the position is linear in the percent fall.
- Outcome: a rise over the next 3 days (Monday to Wednesday), larger after deeper falls -> kept: a long from Sunday's close, held 3 daily bars.
- Verdict transfer: yes: the forecast is exactly the percent depth of the weekend fall, held over Monday to Wednesday, so its 3-day result is the idea's claim.
Forecast: A weekday detector selects only the bar whose coming bar is Monday, which is Sunday's bar. On that bar the forecast is the Sunday one-day percent return (PriceEvolutionOnPeriodComponent, period 1), standardised over its last 500 daily values, then negated and clipped at 0. On every other day the regime is null and the forecast is 0. On a Sunday that fell, the forecast is positive and grows linearly with the percent depth of the fall: a fall the size of the coin's 500-day mean absolute daily move gives about +10, capped at +20. A Sunday that rose gives 0. The forecast is never negative.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Over all cases (a Sunday bar with forecast above 0, each coin and window), the least-squares slope of the coin's Monday-to-Wednesday return on the Sunday forecast, with its t. The return is close[t+3] / close[t] - 1 minus the coin's normal 3-day drift (its mean 3-day return over all windows). The cases do not overlap.
- Supporting check: The mean of the same drift-adjusted 3-day return over the cases is above 0.
- Confirm: The idea is confirmed if the slope is positive with t >= 2 and the mean drift-adjusted 3-day return of the cases is above 0.
- Reject: The idea is rejected if the slope is negative with t <= -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive. So is a slope with t >= 2 whose cases' mean drift-adjusted return is 0 or below. The test needs at least 100 cases across coins and windows; fewer is inconclusive.
