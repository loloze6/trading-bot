---
idea: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: a daily close above the prior 20-day closing high, then a close back below that high within 3 days -> adapted: the binary event is graded by how deep the close sits under the old high, and "after" becomes "while it stays below" (breakout 1 to 3 bars before).
- Comparison: the smaller the coin's 20-day return before the breakout, the larger the fall -> kept: measured in the criterion from the recorded closes, as the pre-breakout return of each case.
- Outcome: the coin falls over the next 5 days -> kept: 5-bar short-side return after each case, against the coin's normal drift.
- Verdict transfer: yes: the forecast shorts exactly the failed breakouts the idea names, and the criterion tests both the fall and its link to the pre-breakout run-up.
Forecast: The forecast is built from one component, `FailedBreakoutDepthComponent`. Its settings are period 20, fail_window 3, source close, reference prior_high and exclude_current 1. It finds the most recent close, 1 to 3 bars ago, that rose above the highest of its prior 20 closes. If today's close is back below that old high, it reads the percent depth under it. Otherwise it reads 0. This value is standardised over its past 250 values and then negated. The forecast is therefore 0 when there is no failed breakout. It is negative (short) while a failed breakout is live, and the short grows as the close sinks further under the old high. It is never positive (short only).
Config: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: A case is a short bet: the forecast falls by at least 2 points on the short side, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from that bar's close, minus the coin's normal 5-bar drift over all windows, in the short direction. The measure is the t of the mean over all cases, all coins pooled.
- Supporting check: For each case, compute the pre-breakout 20-day return from the recorded closes: close[j-1]/close[j-21]-1, where j is the breakout bar. Fit the least-squares slope of the case's short-direction unusual move on that return. It must be negative with t ≤ -2: a smaller run-up gives a larger fall.
- Confirm: The main measure has t ≥ 2 on at least 30 independent cases, and the supporting-check slope has t ≤ -2.
- Reject: Either of two results rejects the idea: - The main measure has t ≤ -2: the coin rises more than its drift after failed breakouts. - The main measure is positive but the slope has t ≥ +2: the fall is larger after larger run-ups.
- Inconclusive: Every other result is inconclusive, including a main measure with t between -2 and 2, or a confirmed fall with a slope t between -2 and 2. Fewer than 30 independent cases is inconclusive whatever the t.
