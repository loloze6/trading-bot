---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The forecast is active only on a day whose close is above the previous close and whose volume is below 75% of its 24-day average volume, where the average includes that day. On those days the forecast is negative: a short whose size grows with how sharp the day's rise was. The raw value is the day's close-to-close return in percent (PriceEvolutionComponent, period 1). It is standardised against its own previous 60 daily values (min_periods 20), so a typical absolute day sits near 10. The sign is then flipped. A signed power with exponent 2 and pivot 10 follows, so small rises give almost no short and sharp rises give a large one: a rise twice the typical size reaches the cap of -20. On every other day the forecast is 0 (flat). It is never positive. The minimum rebalance size is set to 0 so that small shorts are opened and every short is closed the next day.
Config: 003-01_low-volume-up-move-reverts_config.json
Confirm: Horizon is 1 bar: the day after each event day, an event day being one where the forecast is below 0. The main measure is pooled over all event days in the 6 windows. For each event day, compute the position times the next day's coin return in excess of that window's mean daily return, which strips out the coin's own drift (the holding benchmark). Each event counts once, since the 1-bar horizons do not overlap. The idea is confirmed if this excess P&L has a positive mean with t ≥ 2 over at least 30 events. The supporting check is that the events in the top half by |forecast| have a more negative mean excess next-day coin return than the bottom half.
Reject: The idea is rejected if the pooled mean excess P&L per event is zero or negative, meaning the coin does not fall, relative to its drift, on the day after low-volume up days.
Inconclusive: Any of these neither confirms nor rejects the idea: a positive mean with t below 2, fewer than 30 events in total, or a positive mean where the larger shorts do not do better than the smaller ones.
Deviation: "Followed by falling back" is tested as the next day's return only, with a one-day short held while the condition is true. "Sharp move" becomes the size of a single day's close-to-close rise, graded, rather than a multi-day surge. "Unusually low volume" becomes volume below 75% of a 24-day average that includes the same day, a fixed threshold that switches the position on and off. The brief's contrast with high-volume moves is not tested here.
