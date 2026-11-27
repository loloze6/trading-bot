---
idea: 076-01_run-break-three-day-fade
brief: 076_run-break-fade-any-market
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 33ea5162b274
---
Fidelity:
- Situation: the first up day after a run of down days -> adapted: "after X" made "while X", a regime holding only on the bar whose close breaks a down run of one or more days.
- Comparison: the fall grows with the number of down days in the run -> adapted: the threshold made graded, so the short size grows with the run's count of down days.
- Outcome: a fall over the next three days -> kept: each bet is held 3 daily bars, short only.
- Verdict transfer: yes: the config shorts exactly the run-breaking up days, scaled by run length, for three days, so its result reads directly on the idea.
Forecast: The forecast uses `PriorDownRunOnUpCloseComponent` (max_bars 30, form "count"). On a bar that closes above the prior close, it counts the down closes in the run just broken. On every other bar it is 0. The regime detector selects `mean_reversion` only when that count is 1 or more, which is a run-breaking up day. Every other bar goes to `unknown`, which is null, so the book is flat there. Inside the regime, the same count is standardised and then negated, so the forecast is never positive: - The 60-bar past mean includes the zeros of non-breaking bars. - Break bars are about a quarter of bars, so the target is set to 2.5. A single-day run then gives about -5, two days about -10, three about -15, and four or more reach the cap of -20. - This keeps the forecast graded instead of pinned at the cap. The forecast is zero off break bars. Each short bet is held for the 3-bar horizon.
Config: 076-01_run-break-three-day-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 3 bars
- Main measure: On run-breaking up days, take the coin's 3-day return from the close minus its normal 3-day drift, read short (the unusual move). Counted once per 3-bar grid cell, with the t over days, cases of one day taken together; before costs.
- Supporting check: Take the same unusual move (short-signed) after runs of 3 or more down days, minus after runs of exactly 1 down day (Welch t).
- Confirm: The main unusual move is positive with t ≥ 2, and the check difference is positive with t ≥ 2.
- Reject: The main unusual move is negative with t ≤ -2 (break days followed by rises beyond drift). Or the check difference is negative with t ≤ -2 (single-day runs fade more than long runs).
- Inconclusive: Any other result is inconclusive, including t between -2 and 2 on either measure. At least 100 cases are needed, at least 30 of them after runs of 3 or more down days.
