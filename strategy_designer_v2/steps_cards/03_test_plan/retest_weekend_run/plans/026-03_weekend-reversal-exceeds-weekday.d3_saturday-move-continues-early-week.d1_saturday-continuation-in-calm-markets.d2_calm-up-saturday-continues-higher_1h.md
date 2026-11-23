---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d2_calm-up-saturday-continues-higher
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin's rise over Saturday's 24 hours, with the position larger for a larger rise and no short after a down Saturday -> replaced: no component gives a plain 24-bar return lagged 24 bars; the only lagged one, `VolatilityScaledReturnComponent`, divides it by volatility.
- Comparison: the coin's 30-day volatility of hourly returns is low against its own past year, and the position grows the calmer the coin is -> replaced: a regime rule on the volatility percentile would keep "low" but drop "the calmer, the larger"; no catalogue component multiplies the rise by calmness.
- Outcome: a further rise over Monday and Tuesday that grows with Saturday's rise -> kept: a regime fires on the bar before Monday 00:00 and the bet is held 48 bars.
- Verdict transfer: no: with the rise measured in volatility units and the calmness grading lost, neither a confirm nor a reject would speak for the idea as stated.
Reason: The Monday-open timing (`WeekdayComponent` and `HourOfDayComponent` in a regime rule) and the 48-bar hold can be built. The forecast cannot. It needs Saturday's plain 24-bar rise, read 24 bars back, times the ratio of the coin's past-year 30-day volatility to its current 30-day volatility. No component computes that, and a weighted mean of separate components cannot form the product.
