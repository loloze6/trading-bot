---
idea: 086-01_heavy-volume-up-day-continuation
brief: 086_falling-calm-heavy-volume-up-day-accumulation
data-instruments: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling calm market, a day closing up on volume heavy against its 20-day average -> adapted: falling calm is the profile, added by code; the up close is a regime rule (1-day return above 0); "heavy" is a regime rule at the convention of 1.5x the prior 20-day mean volume, with the position graded by the volume ratio inside it.
- Comparison: the heavier the day's volume against its 20-day average, the larger the rise -> adapted: the position grows with the volume ratio, graded above the regime's level.
- Outcome: the price rises over the next 5 days -> kept: each bet is held 5 bars and judged on the 5-day return after the signal day.
- Verdict transfer: yes: the book holds only heavy-volume up days in falling calm markets, sized by volume, for 5 days, which is the idea as stated.
Forecast: The regime is active only on a bar whose close is above the prior close and whose volume is at least 1.5 times its mean over the prior 20 days. The profile code also keeps the book flat outside falling calm markets. Inside the regime the forecast is the day's volume ratio minus 1, standardised over its past 60 values and clipped at 0, so it is long only. A ratio of 1.5 gives about +10 and a ratio of 2 or more reaches the cap near +20. The forecast is 0 on every other bar, and each bet is held 5 bars.
Config: 086-01_heavy-volume-up-day-continuation_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case: the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows. A case is a forecast rise of at least 2 points, read once per 5-bar grid cell. The measure is the mean of these unusual moves, with its t, taking the cases of one day together.
- Supporting check: Split the cases at the median volume ratio, read from `last_history_value` plus 1. The mean unusual move of the heavier half minus that of the lighter half must be above 0.
- Confirm: The mean unusual move is above 0 with t >= 2, and the supporting check is above 0.
- Reject: The mean unusual move is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming main measure with a failed supporting check. Fewer than 30 cases, or fewer than 20 distinct days, is inconclusive whatever the result.
