---
idea: 086-02_volume-weighted-up-move-continuation
brief: 086_falling-calm-heavy-volume-rise-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling, calm market, a day's up move times its volume against the 20-day average -> kept: the 1-day return in usual moves times volume over its 20-day mean; the profile is added by code.
- Comparison: larger product versus smaller product, so heavier-volume up days versus lighter ones -> adapted: graded, the position grows with the product.
- Outcome: price rises over the next 5 days, more for a larger product -> kept: long, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's product, inside its profile, held over its horizon, and it is judged by whether larger products bring larger 5-day rises.
Forecast: One component, VolumeWeightedScaledReturnComponent (vol_period 20, volume_period 20). Its raw value is the day's return divided by the 20-day standard deviation of daily returns, times the day's volume over its 20-day mean volume. Standardise puts it on the scale of its own past 60 values (target 10, cap 20). A clip at 0 then keeps only up days, which gives a long-only forecast. The forecast is 0 on down and flat days. It is positive on up days and grows continuously with the size of the up move and with how heavy the volume is. The falling-calm profile is applied by code, so the book is flat outside it.
Config: 086-02_volume-weighted-up-move-continuation_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the signals: a rise of the forecast of at least the 2-point band, read once per 5-bar grid cell. For each case, take the coin's 5-bar return from the signal's close minus the coin's normal 5-bar drift. The measure is the mean of these unusual moves over the cases, with its t, counting the cases of one day together.
- Supporting check: The mean unusual move of cases whose forecast is above the median case forecast, minus that of cases below it. This difference must be above 0.
- Confirm: The mean unusual move is positive with t ≥ 2, and the supporting difference is above 0.
- Reject: The mean unusual move is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2. A t of 2 or more with a supporting difference at or below 0 is also inconclusive. At least 30 cases on at least 30 distinct days are needed; with fewer, the result is inconclusive.
