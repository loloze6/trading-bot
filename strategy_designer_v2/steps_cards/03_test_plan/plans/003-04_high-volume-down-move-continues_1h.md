---
idea: 003-04_high-volume-down-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: On every 1h bar, take the bar's own move, the one-bar close-to-close change in percent (PriceEvolutionComponent, period 1). The idea is active only on a bar that closes down AND whose volume is at or above its 20-bar mean volume. On those bars the forecast is a short sized by how sharp the move is: 10 × (the bar's move ÷ the mean absolute one-bar move of the previous 60 bars), capped at −20 and never above 0. A fall of typical size gives about −10 (100% short), a fall twice the typical size gives −20, and a tiny fall gives a near-zero short. On every other bar (an up bar, or volume below its 20-bar mean) the forecast is 0 (flat). The condition is re-checked at each close, so a short is held for the next bar only, unless the next bar is again a heavy-volume down bar.
Config: 003-04_high-volume-down-move-continues_1h_config.json
Confirm: The horizon is 1 bar: the bar after each signal bar, a heavy-volume down bar with a non-zero forecast. Pool all six windows and measure the next-bar return minus the coin's mean 1h return in that window. Its mean is negative with a t-statistic of −2.0 or below, over at least 300 signal bars, counting each next-bar return once, before costs. Supporting check: the regression of that excess return on the forecast has a positive slope (larger shorts are followed by larger falls) in at least 4 of the 6 windows.
Reject: The mean excess next-bar return after signal bars is zero or positive (t ≥ 0) over at least 300 signal bars. That would mean heavy-volume falls do not continue, or they reverse.
Inconclusive: A t-statistic between −2.0 and 0, or fewer than 300 signal bars in total.
Deviation: The config tests something narrower than the idea in four ways: - "Unusually high volume" becomes volume at or above its 20-bar mean, which is above average rather than unusually high. - "Sharp" is not a threshold. Every down bar on heavy volume counts, and the short is scaled by the move's size relative to the last 60 bars, so small falls get small positions. - "Followed by" is tested over one bar, because the position lasts only while the condition holds. - The move is one 1h bar, not a multi-bar move.
