---
idea: 077-02_choppy-calm-swing-fall-carries
brief: 077_choppy-calm-swing-scaled-moves-carry
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ad4516fba127
---
Fidelity:
- Situation: in the profile, a 14-day return that is large and negative -> kept: the regime holds only bars where the 14-day return in usual moves is -2 or lower; "large" takes the conventional 2-sigma level, and the short is graded by the size of the fall inside it.
- Comparison: against the coin's own daily swing over the past 30 days -> kept: the return is divided by the standard deviation of the last 30 daily returns times sqrt(14), a constant factor.
- Outcome: the coin keeps falling over the next 7 days, more after a larger scaled fall -> kept: a short held 7 bars, sized by the scaled fall.
- Verdict transfer: yes: the book shorts only after large swing-scaled 14-day falls in choppy calm markets, sized by the fall, and is judged on the next 7 days.
Forecast: The forecast uses `VolatilityScaledReturnComponent` (`period` 14, `vol_period` 30). This is the 14-day return divided by the 30-day daily-return standard deviation times sqrt(14). The regime detector reads the same measure and sends a bar to `mean_reversion` only when it is -2 or lower; every other bar is flat. The choppy calm profile is added by code. Inside the regime the forecast is the measure standardised over its last 60 values (`min_periods` 20), clipped at 0. It is negative (short) and grows in size with the swing-scaled fall, up to the -20 cap. It is zero outside the situation and never long.
Config: 077-02_choppy-calm-swing-fall-carries_1d_config.json
Profile: choppy calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: The cases are short signals: a fall of the forecast of at least 2 points, read once per 7-bar grid cell of each window. For each case, take the coin's 7-day return from the signal bar's close minus the coin's normal 7-day drift (all windows), signed for a short. The measure is the mean of these unusual moves and its t, with cases on the same day taken together.
- Supporting check: Across the cases, the slope of the short-signed unusual move on |forecast| at the signal bar is positive: larger scaled falls are followed by larger further falls.
- Confirm: The mean short-signed unusual move is above 0 with t >= 2, over at least 20 distinct case days, and the slope on |forecast| is above 0.
- Reject: The mean short-signed unusual move is below 0 with t <= -2 (the coin rebounds) over at least 20 distinct case days.
- Inconclusive: Any t between -2 and 2. Also a confirming mean whose slope is not positive, and fewer than 20 distinct case days.
