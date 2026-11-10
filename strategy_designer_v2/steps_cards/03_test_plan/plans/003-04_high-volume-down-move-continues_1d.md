---
idea: 003-04_high-volume-down-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Active only on a day whose close-to-close return is negative and whose volume is at or above its 20-day average volume; on every other day the forecast is 0 (flat). On an active day the forecast is short and sized by how sharp the drop is. The size is the day's percent return divided by the mean absolute daily return of the previous 60 days, times 10, capped at -20, with the long side clipped away. A drop of typical size gives about -10 (100% short). A drop twice the typical size gives the -20 cap. A tiny drop gives a near-zero position. The position is re-decided at each daily close, so it is held for one day and continues only if the next day is again a heavy-volume down day.
Config: 003-04_high-volume-down-move-continues_1d_config.json
Confirm: The horizon is 1 bar (the next day). Pool all active days across the 6 windows; returns at this horizon do not overlap. For each active day, take position size times the next day's return minus that window's mean daily return, which removes the coin's own drift as buy-and-hold would earn it. This position-weighted, drift-adjusted short gain must be positive with a t-statistic of at least 2.0, and positive in at least 4 of the 6 windows. Supporting check: on down days with below-average volume, read from the recorded move value and price, the same drift-adjusted next-day short gain is lower than on the heavy-volume down days.
Reject: The pooled drift-adjusted short gain is zero or negative, meaning heavy-volume down days are on average followed by a rebound relative to drift. Or the next-day short gain after heavy-volume down days is no larger than after low-volume down days of similar size.
Inconclusive: The pooled gain is positive but its t-statistic is below 2.0, or it is positive in fewer than 4 of 6 windows. Also inconclusive: fewer than 60 active days in total.
Deviation: "Unusually high volume" becomes "volume at or above its 20-day average", a binary condition with no multiple. "Sharp" is not a threshold: every heavy-volume down day is active, with the short sized by the drop relative to typical daily moves. "Followed by further falling" is tested only over the next single day, and the position continues only while new heavy-volume down days occur. Only the downward half of the brief is tested.
