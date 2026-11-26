---
idea: 068-02_falling-agitated-run-break-fade
brief: 068_falling-agitated-first-bounce-fades
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 503ce793b4fe
---
Fidelity:
- Situation: in a falling, agitated market, a day that closes up after an unbroken run of down days -> kept: the profile is added by code, and the regime fires only when `PriorDownRunOnUpCloseComponent` is 1 or more.
- Comparison: the longer the down run just before the up day -> kept: the forecast is graded by that component's run length (1 to 30 days).
- Outcome: the coin falls over the next day, more after longer runs -> kept: a short held for 1 bar, larger after longer runs.
- Verdict transfer: yes: the test bets short exactly on these up days, sized by the prior run length, for the next day.
Forecast: The regime detector selects `mean_reversion` only on a day that closes up after at least one down day. On that day the forecast is short, sized by how many down days came just before it. The run length is standardised against its own past 60 values and negated. A clip at 0 keeps it short only. On every other bar the forecast is 0. Because most past values are 0, standardised values are large: a 1-day run gives about -12 to -20, and longer runs sit at the -20 cap. So the grading mainly separates 1-day runs from longer ones.
Config: 068-02_falling-agitated-run-break-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast below 0, regress the next-day return, minus the coin's mean daily return over all windows, on the run length (`debug_info.components.down_run.last_history_value`). Cases on the same day are summed, and the slope's t is reported.
- Supporting check: On those same bars, the mean short-side unusual move (minus drift, sign flipped for a short) is above 0.
- Confirm: The slope is negative with t ≤ -2, and the supporting check passes.
- Reject: The slope is positive with t ≥ +2, or the mean short-side unusual move is below 0 with t ≤ -2.
- Inconclusive: Any slope t between -2 and +2, or a slope t ≤ -2 with a mean unusual move not above 0. The minimum is 100 cases on at least 60 distinct days; fewer cases is inconclusive.
