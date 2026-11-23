---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 6d77ef5ed57a
---
Fidelity:
- Situation: a weekend fall (the Saturday-to-Sunday close-to-close return) of a large multiple of the coin's usual daily move -> adapted: "large multiple" made graded: the depth of the Sunday bar's fall, divided by the coin's usual daily move, is damped by a cubic dead zone; the weekend is kept as a regime on the coming weekday (Monday).
- Comparison: only while the 20-day usual daily move is high against its past-year usual move -> kept: a regime rule requires the 20-day/365-day volatility ratio to be at least 1, and the size also grows with that ratio.
- Outcome: the coin rises over the next 3 days (Monday to Wednesday), more with a deeper fall and a higher ratio -> kept: a long position on Sunday's close, held for 3 daily bars.
- Verdict transfer: yes: the forecast is long only after weekend falls in turbulent stretches and grows with both the fall's depth and the volatility ratio, so its 3-day outcome confirms or rejects exactly this claim.
Forecast: The forecast is active only on the bar whose coming bar is a Monday (the Sunday bar, decided at Sunday's close), and only when the 20-day volatility of daily returns stands at or above its 365-day mean. The volatility here is `VolatilityRatioToAverageComponent` with vol_period 20 and vol_lookback 365. On every other bar the forecast is 0. On active bars the forecast reads `VolatilityScaledReturnComponent` with period 1, vol_period 20 and vol_lookback 365. This is the Sunday bar's return divided by the past-year mean of the 20-day volatility. It equals (the fall in 20-day usual moves) x (the 20-day volatility over its yearly mean), so it grows with both the fall's depth and the turbulence. The pipeline is standardise (window 385, min_periods 96), then negate (a fall reads positive), then clip at a minimum of 0 (long only). Last comes signed_power with exponent 3, the strongest graded dead zone, so ordinary weekend dips give near-zero positions. Large falls in turbulent stretches give large longs, capped at 20.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are Sunday-close bars with forecast >= 2, a bet. For each case, take the coin's return close[t+3]/close[t]-1, inside the window, minus that coin's normal 3-day drift (its mean 3-bar return over all windows). The measure is the mean of this unusual move over all cases and coins, with its ordinary t.
- Supporting check: Split the cases at their median forecast. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The mean unusual move is positive with t >= 2, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 whose supporting check fails is also inconclusive. So is any result with fewer than 100 cases in total.
