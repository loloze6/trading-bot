---
idea: 003-05_up-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp upward move -> adapted: the current 1h bar's rise, graded by size, with down bars kept flat.
- Comparison: thin versus heavy volume behind moves of similar size -> adapted: two regimes split by whether the bar's volume is below or above its 20-bar mean, with both legs graded by the same move size.
- Outcome: thin rises give back more than heavy rises, which hold -> adapted: short thin rises and long heavy rises while the bar is current, with no holding period; the share given back is judged over a fixed horizon from the recorded prices.
- Verdict transfer: yes: the forward returns after thin and heavy rises of matched size are compared directly, so a confirm or reject applies to the idea itself.
Forecast: The indicator is the 1-bar percent change of the close (PriceEvolutionComponent, period 1). It is standardised against its last 60 values (min_periods 20) and clipped at 0, so only rises count. It then goes through signed_power with exponent 2, so small rises give a small position and sharp rises a large one. A veto on the same 1-bar move uses volume_filter (period 20). The filtered value is zero exactly when the bar's volume is below its 20-bar mean, and that selects mean_reversion. In mean_reversion the graded rise is negated, giving a short that grows with the size of the thin rise. On all other bars (the default, unknown) the same graded rise is held long, growing with the size of the heavy rise. The forecast is zero on down or flat bars.
Config: 003-05_up-move-retrace-by-volume_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: Take each bar with a non-zero forecast. Compute its 6-bar forward return of the close, minus the coin's mean 6-bar return in that window, divided by the bar's own rise: the share kept, negative when the rise is given back. Within quintiles of the standardised rise size, compare the mean share kept on heavy bars (forecast > 0) with thin bars (forecast < 0), pooled over the 6 windows. Use only one case per 6-bar block so overlapping returns count once.
- Supporting check: Gross portfolio return before costs, minus buy-and-hold of the coin, in each window. It should be positive in at least 4 of 6 windows.
- Confirm: The share kept is higher on heavy rises than on thin rises in at least 4 of 5 size quintiles, and the pooled size-matched difference is positive with t ≥ 2 on the non-overlapping cases.
- Reject: The pooled size-matched difference is zero or negative (thin rises keep as much as or more than heavy ones), or heavy rises give back more in at least 3 of 5 quintiles with t ≤ -2.
- Inconclusive: A positive difference with t below 2, or quintile results that are split. At least 300 non-overlapping cases are needed on each side, with at least 30 per side in every quintile; below that the test is inconclusive.
