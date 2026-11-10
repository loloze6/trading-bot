---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The forecast is active only on a daily bar that closes up on volume below its 20-bar average, where the average includes that day. A regime rule detects this with VolumeExpansionHedgeComponent (vol_period 20, raw value below 0). On every other bar the forecast is 0 (flat). On an active bar the forecast is short, sized by how sharp the day's rise was. The day's percent change (PriceEvolutionComponent, period 1) is divided by the mean absolute daily change of the 60 bars before it, times 10, capped at 20. It is then negated, passed through signed_power (exponent 2, pivot 10) and clipped at a maximum of 0. A rise of typical size gives about -10, i.e. 100% short. Half a typical rise gives -2.5. A rise of 1.4 times typical or more gives -20. The forecast is never positive.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Confirm: The horizon is 1 bar. The main measure is BTC's mean next-day return after the active bars, minus BTC's mean daily return over all bars of the same six windows. Each event counts once, because the returns do not overlap. The idea is confirmed if this excess return is negative with t ≤ -2, pooled over all windows, before costs. As a supporting check, events in the top half of |forecast| should show a more negative next-day return than events in the bottom half.
Reject: The idea is rejected if the excess next-day return after active bars is ≥ 0. It is also rejected if the strongest-signal half shows a next-day return no lower than the weakest half, which would mean sharper thin-volume rises do not revert more.
Inconclusive: An excess return that is negative but with -2 < t < 0 is inconclusive. So is a pooled sample of fewer than 60 active bars.
Deviation: "Unusually low volume" becomes "volume below its 20-bar average", which covers more days than truly unusual ones. "Followed by a fall" is tested only over the next single day. The short position lasts one bar unless the next day is again a thin-volume up day. "Sharp" is not a cutoff: the short size grows with the day's rise, so small up days get small or untraded shorts. Only the low-volume half of the brief is tested. The high-volume continuation case is not part of this config.
