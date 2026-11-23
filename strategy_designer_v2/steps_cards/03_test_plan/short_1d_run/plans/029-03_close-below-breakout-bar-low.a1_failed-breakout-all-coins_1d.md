---
idea: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a close above the prior 20-day high, then, within a few days, a daily close below the breakout day's low -> adapted: "after the failure" becomes "while the most recent 20-day-high breakout of the last 3 days sits below its low", graded by the depth of the close under that low.
- Comparison: the further the close sits below the breakout day's low, the larger the fall -> kept: the position grows with that depth in percent.
- Outcome: the coin falls over the next 5 days -> kept: short, held 5 daily bars.
- Verdict transfer: yes: the forecast is short exactly on failed breakouts closing under the breakout low, sized by that depth, and judged on the next 5 days' fall.
Forecast: One component, FailedBreakoutDepthComponent, with period 20, source "high" (a close above the highest high of the prior 20 days), fail_window 3 (the brief's "within a few days"), reference "breakout_low", exclude_current 0 and lag 0. On each daily close it finds the most recent breakout bar of the last 3 days. It then measures how far the current close sits below that bar's low, in percent of the low. The value is 0 when there is no breakout in the window, or when the close is at or above the breakout low. The value is standardised over its past 60 values (target 10, cap 20) and negated. The forecast is therefore 0 on ordinary days and negative (short) only on failed breakouts. The short grows with the depth under the breakout low and never goes above 0, which keeps the strategy short only.
Config: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the bars where the forecast makes a short bet (it falls by at least 2 points on the short side), read once per non-overlapping 5-bar grid cell. For each case, take the coin's 5-bar return from the signal's close minus the coin's normal 5-bar drift over all windows, signed short (a fall counts positive). Measure the mean of these unusual moves, with the t of the mean, pooled over all coins and windows, before costs.
- Supporting check: Across the cases, the Spearman correlation between the depth at the signal (abs of post_pipeline_value of fail_depth) and the short-signed unusual move is above 0.
- Confirm: The mean short-signed unusual move is above 0 with t >= 2 over at least 30 cases, and the supporting correlation is above 0.
- Reject: The mean short-signed unusual move is below 0 with t <= -2 over at least 30 cases, meaning the coin rises more than its drift after failed breakouts.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirm-strength mean whose depth correlation is 0 or below is also inconclusive. So is any result from fewer than 30 cases.
