---
idea: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a close above the prior 20-day high, then within a few days a daily close below the breakout day's low -> adapted: the on/off "close below the breakout low" becomes the graded depth of the close under that low (BreakoutLowDepthPerRunUpComponent, period 20, fail_window 3 for "a few days").
- Comparison: the smaller the 20-day rise into the breakout day, the larger the fall -> kept: the depth is divided by (1 + the 20-day run-up into the breakout bar in percent).
- Outcome: the coin falls over the next 5 days -> kept: a short held for 5 daily bars.
- Verdict transfer: yes: the forecast is the idea's failed breakout, discounted by the idea's run-up and held for its 5-day horizon, so its result is the idea's result.
Forecast: One component, BreakoutLowDepthPerRunUpComponent (period 20, fail_window 3, rise_period 20). Its raw value is the close's percent depth below the low of the most recent bar of the last 3 that closed above the prior 20-day high, divided by (1 + that bar's 20-day rise in percent). It is standardised over its 60 past values and then negated. The forecast is zero when there is no failed breakout below the breakout bar's low. It is negative (short) during one, and grows more negative as the close sinks deeper under the breakout low and as the rise into the breakout gets smaller. It is never positive, because the brief is short only.
Config: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: A case is a short bet: a fall of the forecast of at least 2 points, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all its windows, with the sign flipped to the short side. Measure the mean of this over all cases, with its t.
- Supporting check: Across the cases, the Spearman correlation between |forecast| at the signal bar and the short-side unusual move is above 0. A larger short should be followed by a larger fall.
- Confirm: The mean short-side unusual move has t >= 2 over at least 30 cases, and the supporting correlation is above 0.
- Reject: The mean short-side unusual move has t <= -2 over at least 30 cases, meaning the coin rises more than its drift after the failure.
- Inconclusive: Any t between -2 and 2. Also inconclusive: t >= 2 with a correlation at or below 0, or fewer than 30 cases across all coins and windows.
