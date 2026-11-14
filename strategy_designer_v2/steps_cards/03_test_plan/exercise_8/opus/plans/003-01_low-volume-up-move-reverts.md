---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Active only on a day whose volume is below its 20-day average volume. That condition is set by a regime veto: volume_filter (period 20) applied to a constant +10 gives 0 on low-volume days, and the veto fires when that value is below 5. On those days the forecast is short and sized by the day's rise: - the 1-day close-to-close return (PriceEvolutionComponent, period 1), divided by the mean absolute 1-day return of the previous 60 days (standardise, window 60, min_periods 20, target 10, cap 20); - then negated, then clipped to at most 0, so down days give 0; - then passed through signed_power (exponent 2, pivot 10), so small rises give a tiny short and sharp rises a large one. The result runs from 0 (flat or down day) to about -40, clipped at -20 by the engine. On normal or high-volume days the regime is null and the forecast is 0. It is never positive.
Config: 003-01_low-volume-up-move-reverts_config.json
Confirm: Horizon is 1 bar (the position is set at the close of the thin-volume up day and held over the next day). Pool all active bars (forecast < 0) across the 6 windows; non-overlapping one-day returns count once. Regress the next day's coin return, minus that window's mean daily return, on the forecast. Confirm if the slope is positive (bigger shorts are followed by lower-than-average returns) with t ≥ 2. Supporting check: the forecast-weighted sum of demeaned next-day returns is favourable to the short in at least 4 of the 6 windows.
Reject: Reject if the pooled slope is zero or negative: after thin-volume rises, the next day's demeaned return is no lower, or is higher, the larger the rise.
Inconclusive: A positive slope with t between 0 and 2, or fewer than 60 active bars in total. Also a slope with t ≥ 2 that is favourable in only 3 or fewer windows.
Deviation: - "Unusually low volume" becomes volume below its own 20-day average, a plain threshold rather than an extreme. - "Sharp move" becomes the size of a single day's rise relative to the past 60 days' moves, graded rather than thresholded. - "Followed by price falling back" is tested only over the one day after the move bar, because the position exists only while the condition holds. A slower reversion over several days is not captured. - The brief's contrast with high-volume moves (which should hold) is not tested: those days are flat.
