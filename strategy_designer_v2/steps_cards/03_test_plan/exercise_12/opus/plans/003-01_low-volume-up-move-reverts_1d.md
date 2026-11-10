---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The forecast is active only on a "thin up-move" bar. That is a daily bar that closes above the previous close on volume below its own 20-bar average, with the average including the current bar. On every other bar the forecast is 0 (flat). On an active bar the forecast is short and graded by the size of the day's rise. Take the one-bar percent return, PriceEvolutionComponent with period 1, divide it by the mean absolute one-day return of the previous 60 bars and multiply by 10 (capped at 20). Then negate it and clip it at 0 so it never goes long. A normal-sized up day on thin volume gives about -10 (100% short). A rise twice the usual size gives -20. A tiny rise gives close to 0. The position is held for that one bar and closed at the next close unless the next bar is again a thin up-move.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Confirm: Horizon is 1 bar (the next day), so each event counts once. Pool all active bars across the 6 windows, expecting about 150 or more events. Confirmation requires two things: - The position-weighted mean next-day return of the strategy, minus what holding the coin earned on those same days, is positive with a t-statistic of at least 2. - Supporting check: events with positions at or above the median size show a larger next-day give-back than the smaller ones.
Reject: Rejection is either of two results, before costs: - The next-day return after thin up-moves, weighted by position, is at or above BTC's average next-day return over all bars, so there is no give-back. - The strategy's pooled return on active bars is zero or negative.
Inconclusive: The excess return has the right sign but a t-statistic below 2. Or there are fewer than 30 active bars in total. Or the main measure confirms while larger positions show no larger give-back.
Deviation: "Unusually low volume" becomes "volume below its 20-bar average", an on/off condition, not a graded measure of how thin the volume is. "Sharp" is graded by position size, not imposed as a threshold. "Followed by falling back" is tested only over the next day, because the position must close once the condition ends. The volume half of the brief, that heavy-volume moves hold, is not tested here.
