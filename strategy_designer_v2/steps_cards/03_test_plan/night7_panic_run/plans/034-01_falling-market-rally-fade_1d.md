---
idea: 034-01_falling-market-rally-fade
brief: 034_squeezed-rallies-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: in a falling market, a coin's up day -> kept: the profile is the falling-market condition, and the clip keeps up days only, so the book is flat on down days.
- Comparison: the day's rise in units of the coin's 30-day daily swing -> kept: the one-day return divided by the standard deviation of the last 30 daily returns.
- Outcome: a decline over the next 3 days, larger the larger the scaled rise -> kept: a short sized by the scaled rise, held for 3 bars.
- Verdict transfer: yes: the test shorts exactly the falling-market up days, sized by the rise in swing units, over the idea's 3-day horizon.
Forecast: The forecast uses one indicator: today's one-day return divided by the standard deviation of the last 30 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 30). It is standardised against its own past 60 values. It is then clipped at 0, so only up days count, and negated. The forecast is 0 on down and flat days. On an up day it is negative (short), and the short grows in proportion to the rise in usual moves: an average-sized up day gives about -10, and the size is capped at -20. The falling-market profile is added by code, so the book is flat outside falling markets. Each short is held for 3 bars.
Config: 034-01_falling-market-rally-fade_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move over 3 bars after each case, in the short direction. A case is a short-side forecast rise of at least 2 points, read once per non-overlapping 3-bar grid cell. The unusual move is the coin's 3-bar return from the case bar's close, minus the coin's normal 3-bar drift across all windows. Its t has cases of the same day summed together.
- Supporting check: Size dependence. Across the cases, regress the drift-adjusted 3-bar forward return on the absolute value of `post_pipeline_value`. The slope must be negative with t ≤ -2, meaning a larger scaled rise is followed by a larger decline.
- Confirm: The mean unusual move in the short direction is above 0 with t ≥ 2, and the supporting slope has t ≤ -2.
- Reject: The mean unusual move in the short direction is below 0 with t ≤ -2, meaning up days in falling markets are followed by further rises beyond drift.
- Inconclusive: Any main-measure t between -2 and 2 is inconclusive. A main t ≥ 2 with a slope t above -2 is also inconclusive. At least 30 distinct case days across all coins and windows are needed; with fewer, the result is inconclusive.
