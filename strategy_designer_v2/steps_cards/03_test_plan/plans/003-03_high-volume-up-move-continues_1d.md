---
idea: 003-03_high-volume-up-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Active only on a bar whose close is above the previous close and whose volume is at or above its 20-bar average volume (the 20 bars include the current one). On such a bar the forecast is that day's one-bar percent return divided by the mean absolute one-bar return of the 60 bars before it, times 10, capped at 20, and never below 0. A day whose move is as large as the recent average day is +10 (100% long). A move twice that size or more is +20, and a small move is near 0. On every other bar (down days, or up days on below-average volume) the forecast is 0 (flat). Each position therefore covers the one bar that follows the high-volume up day.
Config: 003-03_high-volume-up-move-continues_1d_config.json
Confirm: Horizon 1 bar, before costs. Take every bar with a positive forecast, pooled over the 6 windows; each next-bar return is used once, with no overlap. The position-weighted mean next-bar return on those bars must exceed BTC's unconditional mean daily return over the same windows, with a t-statistic of at least 2 and at least 30 such bars. Supporting check: the correlation between forecast size and next-bar return is positive.
Reject: The position-weighted mean next-bar return on those bars is at or below BTC's unconditional mean daily return. A t-statistic of -2 or lower (high-volume up moves revert) is a strong rejection.
Inconclusive: The excess is positive but the t-statistic is below 2, or fewer than 30 qualifying bars exist across the windows.
Deviation: Several things change from the idea as written: - "Unusually high volume" becomes volume at or above its 20-bar average, which is a binary regime gate, not a measure of how unusual the volume is. - "Sharp" is graded by the move's size relative to recent daily moves, not required as a threshold. - "Followed by further rise" is tested over only the one bar after the move, because the position closes as soon as the next bar fails the condition. - Only upward moves are tested, so the brief's comparison with low-volume moves of similar size is not made here.
