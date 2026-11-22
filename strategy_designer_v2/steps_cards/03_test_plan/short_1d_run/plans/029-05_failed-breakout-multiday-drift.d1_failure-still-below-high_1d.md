---
idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: a close back below the old 20-day high within 3 days of a breakout, still below it 2 days after the failure -> adapted: "after" becomes "while". A regime is active while the close 2 bars ago sat below the high of a breakout 3 to 5 bars back.
- Comparison: the day-2 close's distance below that old high -> kept: the current close's depth below the old high of the most recent breakout in the last 5 bars, in percent.
- Outcome: price falls from day 2 to day 10 (8 days), and falls more the deeper the day-2 close sits -> kept: a short held 8 bars, sized by the depth.
- Verdict transfer: yes: the gate, the depth sizing and the 8-day short horizon each measure the idea as stated.
Forecast: A regime gate reads `FailedBreakoutDepthComponent` with period 20, fail_window 3, exclude_current 1 and lag 2. It is positive when the close 2 bars ago sat below the old 20-day closing high of a breakout made 3 to 5 bars ago, that is, at least two days after a failed breakout. On gated bars ("trending"), the forecast comes from `FailedBreakoutDepthComponent` with period 20, fail_window 5, exclude_current 1 and lag 0. That component is the current close's percent depth below the old high of the most recent breakout in the last 5 bars. It is standardised (window 60, min_periods 20) and negated, so the forecast is short only. Its size grows linearly with the depth below the old high. It is 0 when the close is back at or above the old high, and 0 on every bar outside the gate.
Config: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d_config.json
Criterion:
- Horizon: 8 bars
- Main measure: The unusual move of each case. A case is a short bet, read once per 8-bar grid cell of each window. Its unusual move is the coin's return over the next 8 bars from the signal bar's close, minus the coin's normal 8-bar drift over all windows, taken in the short direction. The measure is the mean over cases and its t.
- Supporting check: Over the cases, the slope of the short-direction unusual move on the case's absolute forecast is positive.
- Confirm: The mean unusual move is above 0 with t >= 2, over at least 30 cases, and the supporting slope is above 0.
- Reject: The mean unusual move has t <= -2, over at least 30 cases.
- Inconclusive: Any t strictly between -2 and 2, or a confirming mean with a slope at or below 0, or fewer than 30 cases.
