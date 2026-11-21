---
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in 90 days, after a close below it the day before -> adapted: graded by the level's turn count times the close's percent margin above it (the "closes above" condition made graded).
- Comparison: the more times it turned down there, the larger the rise -> kept: the forecast grows with the count of swing-high turns within 2% of the level.
- Outcome: it rises over the next 10 days -> kept: each bet is held 10 daily bars.
- Verdict transfer: yes: the forecast is active only on a fresh upward close through a repeated turning level, scaled by its turn count, and is judged on the next 10 days.
Forecast: The forecast uses ResistanceBreakTouchCountComponent with period 90, side 2, band 2% and cross_period 1. It is zero on every bar except one where today's close is above a 90-day swing-high level and yesterday's close was at or below it. On that bar its raw value is N x (close - level) / level x 100, where N is the number of swing-high turns within 2% of the level. It is standardised against its own last 90 values. The target is 1, because the component is zero on most bars and its past mean absolute value is small. With the default target of 10, nearly every break would sit at the cap of 20 and the forecast would lose its grading. The forecast is never negative, so it is long only. It is positive only on a break and larger the more often the level held and the further the close sits above it. Each bet is held for 10 bars.
Config: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are the forecast's bets, read once per 10-bar grid cell. For each case, take the coin's 10-bar return from the case's close, minus the coin's normal 10-bar drift over all windows. The measure is the mean of that excess return and its t (the ordinary t of the mean).
- Supporting check: Split the cases at the median entry forecast. The mean excess return of the larger half minus that of the smaller half must be above 0.
- Confirm: The mean excess return is positive with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean excess return is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a failed supporting check is also inconclusive. Fewer than 30 cases is inconclusive whatever the t.
