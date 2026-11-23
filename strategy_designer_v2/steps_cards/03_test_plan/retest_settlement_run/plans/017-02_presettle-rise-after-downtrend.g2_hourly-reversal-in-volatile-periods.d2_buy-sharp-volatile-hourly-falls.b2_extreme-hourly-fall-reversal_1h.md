---
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a sharp falling hour -> adapted: "sharp" is made graded, as the size of the hour's fall, and "after" is made "while" (a bet on the bar of the fall).
- Comparison: the fall relative to the coin's usual hourly volatility; ordinary falls give no rise -> kept: the 1h return is divided by the 20-hour return std, and small falls are damped towards 0.
- Outcome: the coin rises over the next 24 hours, more after larger falls -> kept: long, held 24 bars.
- Verdict transfer: yes: the forecast is the idea's fall in its own volatility units, bought and held for its 24 hours.
Forecast: The forecast starts from the current hour's return divided by the standard deviation of the last 20 hourly returns (VolatilityScaledReturnComponent, period 1, vol_period 20). It is standardised over 60 bars, negated so that falls read positive, and clipped at 0, so it is long only and zero on up hours. The strongest graded dead zone (signed_power, exponent 3, pivot 20) then keeps ordinary falls near zero and sizes extreme falls strongly. An average fall gives about 2.5 and a capped extreme fall gives 20. Each bet is held 24 bars.
Config: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The cases are bets: a rise of the forecast of at least 2 points, read once per 24-bar grid cell in each window. For each case, take the coin's 24-bar return from the close of the signal's bar minus the coin's normal 24-bar drift over all windows. Measure the mean of this unusual move over all coins' cases, with its t.
- Supporting check: Split the cases at the median of their forecast. The mean unusual move of the upper half minus that of the lower half must be above 0 (larger falls, larger rise).
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, a confirm-side t whose supporting check fails, or fewer than 30 cases.
