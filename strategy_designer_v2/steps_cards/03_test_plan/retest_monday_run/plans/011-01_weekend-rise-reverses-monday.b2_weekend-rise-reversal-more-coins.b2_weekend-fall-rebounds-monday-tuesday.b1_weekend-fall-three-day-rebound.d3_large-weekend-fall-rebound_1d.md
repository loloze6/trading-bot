---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6d77ef5ed57a
---
Fidelity:
- Situation: the Saturday-to-Sunday close-to-close return is a large fall in usual daily moves -> adapted: the fall in 20-day usual moves, read on the Sunday bar, made graded with a cubic dead zone.
- Comparison: the fall's size against the coin's usual daily move -> kept.
- Outcome: the coin rises over the next 3 days (Monday to Wednesday) -> kept.
- Verdict transfer: yes: the forecast is the weekend fall in usual moves, held exactly over Monday to Wednesday, so its result is the idea's result.
Forecast: The forecast is active only on the Sunday bar, the bar whose coming bar is a Monday (`WeekdayComponent` = 0). On every other bar it is flat. On the Sunday bar it reads that bar's close-to-close return divided by the standard deviation of the last 20 daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 20). That value is standardised against its own past 60 values and negated, so a fall reads positive. It is clipped at 0, so the forecast is long only and zero after a weekend rise. Then a cubic `signed_power` (pivot 10) is applied. Small falls give a forecast near 0, and a fall several usual moves deep gives a large long, up to the cap. The bet is held for 3 bars, Monday to Wednesday.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the Sunday bars where a bet is made (forecast ≥ 2). On each case, take the coin's 3-bar return from the Sunday close, minus the coin's mean 3-bar return over all its windows. The measure is the forecast-weighted mean of that excess return, with its t. Cases fall 7 bars apart, so each case counts once.
- Supporting check: Rank the cases by forecast. The top quartile's mean excess 3-bar return must be greater than the mean of the other cases (Welch t > 0). This shows the rise is carried by the largest falls.
- Confirm: The forecast-weighted mean excess return is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The forecast-weighted mean excess return has t ≤ -2: the largest weekend falls keep falling against the coin's drift.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main measure at t ≥ 2 whose top-quartile check fails is also inconclusive. So is any result from fewer than 100 cases across all coins and windows.
