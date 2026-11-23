---
idea: 029-01_failed-breakout-depth-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a daily close above the prior 20-day closing high, then within the next 3 days a close back below that old high -> adapted: "after X" becomes "while X": the reading is live while that breakout (1 to 3 bars ago) still sits in the window and the close is below the old high.
- Comparison: the deeper the close sits below the old high, the larger the fall -> kept: the forecast is the close's percent depth below the old high, graded.
- Outcome: the coin falls over the next 5 days -> kept: a short held 5 daily bars.
- Verdict transfer: yes: the config shorts exactly the failed breakouts, sized by their depth, over the idea's 5-day horizon.
Forecast: FailedBreakoutDepthComponent (period 20, fail_window 3, source close, reference prior_high, exclude_current 1) finds the most recent bar 1 to 3 days ago whose close beat the prior 20 closes. If today's close is back below that old high, it outputs the depth below it, in percent of the high. Otherwise it outputs 0. The depth is standardised over its past 60 values (min 20), then negated. The forecast is therefore 0 when there is no failed breakout and negative (short) during one, larger in size the deeper the close sits below the old high. It is never positive (short only).
Config: 029-01_failed-breakout-depth-decline_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Cases are short bets (a fall of the forecast of at least 2 points), read once per cell of a non-overlapping 5-bar grid per window. For each case, take the coin's 5-bar return from the signal bar's close, minus its normal 5-bar drift over all windows, in the short direction. The measure is the mean over the cases and its t.
- Supporting check: Across the cases, the Spearman rank correlation between |forecast| and the short-direction excess return is above 0 (deeper failures fall more).
- Confirm: The mean short-direction excess return is above 0 with t >= 2 over at least 30 cases, and the supporting rank correlation is above 0.
- Reject: The mean short-direction excess return is below 0 with t <= -2 over at least 30 cases (the coin rises after failures more than its drift).
- Inconclusive: Any t between -2 and 2, or t >= 2 with a rank correlation of 0 or below, or fewer than 30 cases across all coins and windows.
