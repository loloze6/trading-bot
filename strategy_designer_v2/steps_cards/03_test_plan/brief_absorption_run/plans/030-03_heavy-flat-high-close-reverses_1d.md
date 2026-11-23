---
idea: 030-03_heavy-flat-high-close-reverses
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day of volume far above its 20-day average with a close little changed from the open -> kept: regime rule of volume ≥ 2x the prior 20-day mean and body ≤ 1% of the open.
- Comparison: the closer the close is to the day's high, and the heavier the volume, the larger the move -> kept: graded close location in the day's range times the volume ratio.
- Outcome: the coin falls over the next 5 days -> kept: a short held 5 bars, sized by that product.
- Verdict transfer: yes: the test bets short on exactly those days, graded by close location and volume, over the idea's 5-day horizon.
Forecast: The forecast is active only on days whose volume is at least 2 times the mean of the prior 20 days and whose absolute open-to-close change is at most 1% of the open. On every other day it is 0. On an active day it is minus the standardised product of two things: where the close sits in the day's range (0 at the low, 1 at the high) and that day's volume over its prior 20-day mean. It is scaled against the component's own past 60 values with target 5, so that active days stay graded below the cap. The forecast is never positive. It is near 0 when the close sits at the low, and it becomes more negative (a larger short) as the close nears the high and as the volume gets heavier. Each bet is held 5 bars.
Config: 030-03_heavy-flat-high-close-reverses_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Cases are the short bets (signal days) on the 5-bar grid of each window, pooled over coins and windows. Per case, take minus the 5-bar return from the signal's close minus the coin's normal 5-bar drift (the unusual move on the short side); measure its mean and t.
- Supporting check: Across cases, the correlation between |forecast| on the signal bar and the short-side unusual move is above 0.
- Confirm: The mean short-side unusual move has t ≥ 2 over at least 30 cases, and the correlation check is above 0.
- Reject: The mean short-side unusual move has t ≤ -2 over at least 30 cases (the coin rises more than its drift after these days).
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with a correlation at or below 0, or fewer than 30 cases.
