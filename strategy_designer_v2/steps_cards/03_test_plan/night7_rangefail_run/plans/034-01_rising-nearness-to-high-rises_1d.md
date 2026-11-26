---
idea: 034-01_rising-nearness-to-high-rises
brief: 034_rising-market-nearness-to-high-drift
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f090b5ff5633
---
Fidelity:
- Situation: in a rising market, how close the daily close sits below its 20-day high, in units of its 20-day daily-return standard deviation -> kept: the profile "rising" is added by code, and `VolatilityScaledDistanceFromHighComponent` (period 20, vol_period 20) measures that distance.
- Comparison: closer to the high against further below it -> kept: the forecast is graded by nearness and centred on the coin's own usual distance.
- Outcome: the coin rises more over the next 5 days the nearer it is -> kept: the horizon is 5 bars and gains are judged against the coin's normal drift.
- Verdict transfer: yes: the forecast is the idea's own measure, inside the idea's own profile, at the idea's own horizon.
Forecast: The forecast starts from the close's distance from the highest close of the prior 20 days. That distance is divided by the standard deviation of the last 20 daily returns. It is negative below the high and positive above it. It is standardised over its past 60 values (min 20), which gives about -10 at its usual distance and 0 at the high. A constant of +10 is averaged in with equal weight, so the forecast is (x + 10) / 2: - it is 0 when the close sits at the coin's usual distance below its high; - it is positive and growing as the close nears the high, about +5 at the high and more above it, capped; - it is negative as the close slips further below the high than usual, about -5 at twice the usual distance. The added profile keeps the book flat outside a rising market.
Config: 034-01_rising-nearness-to-high-rises_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: On in-profile bars (regime active, forecast recorded) of the non-overlapping 5-bar grid of each window, regress the coin's 5-day return minus its normal 5-day drift on the forecast. The drift is the coin's mean 5-day return over all its windows. The measure is the slope and its t, with cases of the same day taken together.
- Supporting check: The mean drift-removed 5-day return of grid cases with forecast > 0, minus that of cases with forecast < 0, is above 0.
- Confirm: The slope's t is 2 or more, and the supporting difference is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a t of 2 or more when the supporting difference is not positive. Fewer than 100 independent in-profile grid cases, or fewer than 50 distinct days, is also inconclusive.
