---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a Saturday-to-Sunday close-to-close fall, graded by its size, only while the coin's 20-day return is negative -> kept: the Sunday bar's one-bar fall times the 20-day fall, read at Sunday's close.
- Comparison: the rise grows with the weekend fall and with the depth of the 20-day fall; rising coins are refused -> kept: the forecast is the product of the two falls, and it is 0 when the 20-day return is not negative.
- Outcome: the price rises over the next 3 days (Monday to Wednesday) -> kept: a long held 3 daily bars from Sunday's close.
- Verdict transfer: yes: the forecast is the idea's own graded situation, taken only at Sunday's close and held over its own 3-day horizon.
Forecast: The regime detector reads `WeekdayComponent`. When the coming bar is a Monday (value 0), the bar is Sunday's close and the regime is `mean_reversion`. Every other bar is `unknown`, which is flat. In `mean_reversion` the forecast is `FallTimesFallComponent` with `short_period` 1 and `long_period` 20, that is max(0, −Sunday's one-day return) x max(0, −20-day return) x 100, standardised over its past 60 values (`min_periods` 20). The forecast is 0 when Sunday rose or when the 20-day return is not negative. Otherwise it is positive and grows with both the weekend fall and the depth of the 20-day fall, capped at 20. It is never negative (long only by construction). Each Sunday bet is held 3 bars, through Wednesday's close.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Over the cases (Sunday bars with forecast > 0, one per coin-week, so the cases never overlap), the mean of the coin's 3-bar return close[t+3]/close[t] − 1 minus the coin's normal 3-bar drift (its mean 3-bar return on non-overlapping stretches of all its windows), with the ordinary t of that mean.
- Supporting check: The same unusual 3-bar return in cases whose forecast is above the median case forecast, minus that in cases below it, must be greater than 0 (the larger falls rebound more).
- Confirm: The mean unusual 3-bar return is positive with t ≥ 2 over at least 100 cases, and the supporting check is above 0.
- Reject: The mean unusual 3-bar return is negative with t ≤ −2 over at least 100 cases.
- Inconclusive: Any t between −2 and 2, a confirming t whose supporting check is 0 or below, or fewer than 100 cases.
