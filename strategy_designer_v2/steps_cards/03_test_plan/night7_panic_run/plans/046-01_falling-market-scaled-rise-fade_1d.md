---
idea: 046-01_falling-market-scaled-rise-fade
brief: 046_falling-market-outsized-days-reverse
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: in a falling market, an up day, sized by its rise in units of the 30-day daily-return swing -> kept: the falling trend comes from the brief's profile, and the up day is the one-day return over the 30-day return std, clipped to rises only (exactly 0 on down days, graded on up days).
- Comparison: the rise against the coin's 30-day daily-return swing -> kept: the return is divided by the 30-day std of daily returns.
- Outcome: the coin falls over the next day, more after a larger rise -> kept: a short of 1 bar, sized by the scaled rise.
- Verdict transfer: yes: the book is short only after up days in falling markets, sized by the scaled rise, so its next-day gains test the claim directly.
Forecast: The indicator is VolatilityScaledReturnComponent with period 1 and vol_period 30. It gives the day's return divided by the standard deviation of the last 30 daily returns. It is standardised over its 60 past values, clipped at 0 so that only up days count, then negated. The forecast is exactly 0 after a down or flat day. After an up day it is negative (short), and it grows in size continuously with the rise in usual moves, capped at -20. It is never positive. Outside the falling profile the code keeps the book flat.
Config: 046-01_falling-market-scaled-rise-fade_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The cases are the bars with forecast below 0, using every bar as the 1-bar grid. For each case, take the next-day return minus the coin's mean daily return over all windows, in the short direction. Average it with weights of |forecast|. Its t is computed with the cases of one day summed together, as the workflow defines it.
- Supporting check: Regress the next-day excess return on the forecast over the cases. The slope must be positive: a more negative forecast must be followed by a more negative return.
- Confirm: The weighted mean unusual move is above 0 with t >= 2, and the supporting slope is positive.
- Reject: The weighted mean unusual move is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main t >= 2 with a slope that is zero or negative is also inconclusive. Fewer than 100 cases (case days across all coins and windows) is too few to judge.
