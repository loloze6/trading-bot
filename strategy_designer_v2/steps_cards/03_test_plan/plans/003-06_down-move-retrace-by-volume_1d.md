---
idea: 003-06_down-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp one-bar drop on low versus high volume -> adapted: any down bar, split by whether its volume is below or at/above its 20-bar mean, with position size growing with the drop.
- Comparison: thin drops against heavy drops of similar size -> kept: the next-bar returns of the two groups are compared at equal drop size.
- Outcome: thin drops give back more of the fall next than heavy drops -> adapted: the reversion is measured over the one bar after the drop, since "after X" becomes "while X".
- Verdict transfer: yes: the one-bar group difference, scaled by drop size, is the idea's own contrast, so a clear sign either way carries over to the idea.
Forecast: Each bar's one-day percent move is measured. If it is a down bar on volume at or above its 20-bar mean (heavy), the regime is `trending`. The forecast is the standardised move (window 60, minimum 20), which is negative, so the position is short and sized by the drop (continuation). If it is a down bar on volume below that mean (thin), the regime is `mean_reversion`. The forecast is the same standardised move negated, so the position is long and sized by the drop (reversion). The forecast is about ±10 for a drop of average daily size and caps at ±20 near twice that. On up bars and flat bars the forecast is zero. `min_allocation_change` is 0, so positions follow the forecast exactly and close when the situation ends.
Config: 003-06_down-move-retrace-by-volume_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Share of the drop given back next bar, (next-bar return) / |drop|, averaged over thin down bars minus the same over heavy down bars. All windows are pooled, each bar counts once, and the measure is taken before costs. Comparing two groups of down bars cancels the market's own drift that buy-and-hold would capture.
- Supporting check: The same thin-minus-heavy difference within each tercile of drop size (pooled across groups) has the same sign in at least 2 of 3 terciles.
- Confirm: The thin-minus-heavy difference is above 0 with a Welch t-statistic of 2 or more, and the thin group's mean give-back share is above 0.
- Reject: The difference is at or below 0, or the heavy group's give-back share is at or above the thin group's with a t-statistic of -1 or lower.
- Inconclusive: A positive difference with t below 2, or a negative one with t above -1. The test is also inconclusive with fewer than 20 thin or 20 heavy down bars in total.
