---
idea: 086-02_first-down-day-run-size
brief: 086_rising-agitated-first-dip-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a rising, agitated market, a coin closes down after a streak of consecutive up days -> kept: the profile is added by code, and the down close after an up run is a regime rule (run gain > 0 on that close).
- Comparison: the streak's total gain in units of the coin's daily swing over the last 30 days -> kept: the run's gain over the std of the 30 daily returns ending the day before.
- Outcome: it keeps falling over the next 3 days, more so the bigger the scaled gain -> kept: a short graded by the scaled gain, held 3 bars.
- Verdict transfer: yes: the config measures the stated event, its stated strength and its stated horizon and direction.
Forecast: Bars are taken only inside the rising agitated profile, which code adds. On each bar, `PriorDownRunLossOnUpCloseComponent` is computed with `side` "up", `base` "std", `window` 30, `exclude_current` 1 and `max_bars` 30. On a down close that ends an up run, it gives the run's total gain in standard deviations of the 30 daily returns ending the day before; on every other bar it is 0. The regime detector selects `trending` only when this value is above 0, which is the first down day after an up run. Every other bar is flat. Inside that regime, the forecast is the same value, standardised over the past 60 bars, negated and clipped at 0, so it is short only. Its size grows linearly with the scaled gain of the run. The value is 0 on about three bars in four, and those zeros enter the standardise mean, so the target is set to 2.5 instead of 10. This keeps a typical dip-day reading near -10 rather than pinned at the -20 cap. Each short is held for 3 bars.
Config: 086-02_first-down-day-run-size_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move over 3 bars in the short direction, against the coin's normal 3-bar drift. Cases are the short bets (forecast falls by at least 2 points), read once per 3-bar grid cell. The t aggregates cases by day.
- Supporting check: Across the cases, regress each case's short-direction unusual move on its |forecast|. The slope must be positive with t >= 2.
- Confirm: The mean unusual move is positive with t >= 2, and the supporting slope is positive with t >= 2.
- Reject: The mean unusual move is negative with t <= -2 (the coin rises after the dips), or the supporting slope is negative with t <= -2.
- Inconclusive: Every result in between, including a positive main measure with a slope t under 2. Fewer than 30 cases (or fewer than 30 distinct days) is inconclusive whatever the t.
