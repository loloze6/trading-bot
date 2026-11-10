---
idea: 003-05_up-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp one-day up move on BTC daily bars -> adapted: the daily return ranks in the top decile of its own history, read as a regime condition.
- Comparison: moves on low volume against moves of similar size on high volume -> adapted: "unusually" low or high becomes the bar's volume below, or at or above, its 20-bar mean, used as a regime split.
- Outcome: thin moves give back more of the rise, and heavy moves hold more -> adapted: "afterwards" becomes the next bar while the situation holds, measured as the next return as a share of the move.
- Verdict transfer: yes: both groups face the same size filter and the same one-bar outcome, so if thin moves revert more than heavy ones, that is exactly the idea.
Forecast: On each bar, the detector checks whether the one-bar return ranks at or above the 0.90 percentile of its history. - Heavy case: the move is sharp and the bar's volume is at or above its 20-bar mean. The regime is trending. The forecast is long, equal to the standardised one-bar return: positive and graded with the move's size, capped at 20. - Thin case: the move is sharp and the volume is below its 20-bar mean. The regime is mean_reversion. The forecast is the same standardised one-bar return, negated: short and graded with the move's size. - No sharp up move: the forecast is 0. Each position is held for the next bar only, so the record shows what follows each kind of move.
Config: 003-05_up-move-retrace-by-volume_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: For each sharp-move bar, the next bar's close-to-close return divided by that move's return (the share kept or given back). Compare the mean in thin cases with the mean in heavy cases, pooled over all 6 windows; each case counts once.
- Supporting check: The strategy's portfolio return on active bars, before costs, against holding BTC over the same bars. It should be positive in both the heavy-only and thin-only parts of the record.
- Confirm: The thin mean share is below the heavy mean share, with a Welch t-stat of at least 2.0. The thin mean share is also below 0, meaning part of the rise is given back.
- Reject: The thin mean share is at or above the heavy mean share. Or the thin mean share is at or above 0 while heavy moves revert more.
- Inconclusive: Thin is below heavy but the t-stat is under 2.0. Also inconclusive if there are fewer than 15 thin cases or fewer than 15 heavy cases in total across the 6 windows.
