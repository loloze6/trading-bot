---
idea: 029-04_breakout-extension-failure-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a close above the prior 20-day closing high, a further push above it within 3 days, then a close back below the old high -> adapted: "after the close back below" made "while" the close sits below the old high, for up to 4 bars from the breakout (`FailedBreakoutExcursionComponent`, period 20, fail_window 4), graded by the peak excursion.
- Comparison: the peak excursion above the old high, larger meaning more fall -> kept: the component's value is that excursion in percent of the old high.
- Outcome: the coin falls over the next 5 days, more after larger excursions -> kept: a short held 5 bars, judged against the coin's normal drift.
- Verdict transfer: yes: the forecast is short only on failed breakouts and sized by the excursion, so the record measures exactly the claimed fall and its link to the excursion.
Forecast: The forecast uses `FailedBreakoutExcursionComponent` with period 20 and fail_window 4. Its raw value is 0 unless the coin made a closing break above its prior 20-day closing high within the last 4 bars and is now closing back below that old high. In that case the value is the highest high since the breakout bar, above the old high, in percent of it. `standardise` (60/20) scales this value against its own past, and `negate` turns it into a short. The forecast is 0 on every other bar and never positive. Its size grows with the peak excursion above the old high. Events are sparse, so most of them will reach the -20 cap. The link between excursion size and fall is therefore judged on the recorded raw value.
Config: 029-04_breakout-extension-failure-decline_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short bets: the bars where the forecast falls by at least 2 points below its level since the last bet, read once per 5-bar grid cell. For each case, take the coin's 5-bar return from that bar's close, minus the coin's mean 5-bar return over all windows, signed short. The measure is the mean of this value over the cases, with its t.
- Supporting check: Among the cases, regress the raw 5-bar forward return on the raw excursion (`debug_info.components.fail_exc.last_history_value`). The check passes when the slope is negative with t ≤ -2.
- Confirm: The mean short-signed unusual 5-bar move is above 0 with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean short-signed unusual 5-bar move is below 0 with t ≤ -2 over at least 30 cases, meaning failed breakouts are followed by returns above the coin's drift. Or the excursion slope is positive with t ≥ 2.
- Inconclusive: Any other result is inconclusive: a main t between -2 and 2, a main confirm without the slope check, or fewer than 30 cases.
