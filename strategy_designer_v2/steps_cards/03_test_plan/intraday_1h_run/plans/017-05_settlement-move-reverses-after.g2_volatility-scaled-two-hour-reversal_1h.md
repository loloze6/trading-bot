---
idea: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: a coin's 2-hour move, sized against its usual 2-hour move and scaled up by its 7-day hourly volatility -> kept: the 2-bar return equals (move / usual 2-hour move from the 168-bar volatility) x that volatility, and standardising it over 500 past bars keeps both factors graded.
- Comparison: the move relative to the coin's usual 2-hour move -> kept: it is one factor of that same product, so a larger move in usual units gives a larger forecast.
- Outcome: the move is reversed over the next 2 hours, by more as both factors grow -> kept: the forecast is the negated move, measured on the 2-bar forward return.
- Verdict transfer: yes: the forecast is the idea's own graded fade, and it is judged on the idea's 2-hour horizon.
Forecast: The forecast starts from the coin's 2-bar percent return, which is PriceEvolutionComponent with period 2. Each value is divided by the mean absolute 2-bar return of the 500 bars before it, giving about 10 for a typical move, and capped at ±20. It is then negated. The forecast is short after a rise and long after a fall, and zero only when the 2-hour move is zero. Its size grows linearly with the move in usual 2-hour units times the current volatility against its ~3-week level. No dead zone is used, because the idea is a steady relation and not a rare extreme. It is ungated and long/short.
Config: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Regress the coin's next 2-bar return, close[t+2]/close[t]-1 minus the coin's mean 2-bar return over all windows, on the forecast at bar t. Use non-overlapping bars at positions 0, 2, 4, … of each window, never across windows. Pool all coins and windows, before costs, and report the slope's t-statistic.
- Supporting check: Take the bars in the top quintile of |forecast| on the same grid. The mean of sign(forecast) x excess 2-bar return there must exceed the same mean in the bottom quintile, with Welch t ≥ 2.
- Confirm: The slope is positive with t ≥ 2 on at least 5000 independent cases, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2 on at least 5000 independent cases.
- Inconclusive: The result is inconclusive if the slope t is between -2 and 2, if the slope has t ≥ 2 but the supporting check fails, or if there are fewer than 5000 pooled cases or fewer than 1000 cases in either quintile.
