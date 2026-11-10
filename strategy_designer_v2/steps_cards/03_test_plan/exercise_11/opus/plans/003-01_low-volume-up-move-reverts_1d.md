---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: On each daily close, first check the condition. The bar must close above the previous close, on volume below its 20-day average (the average includes the current bar). On any other bar the forecast is 0 (flat). On a qualifying bar the forecast is short, sized by how sharp the rise was. The rise is today's 1-bar percent change in the close, divided by the mean absolute 1-bar change of the previous 60 days and multiplied by 10. That gives about 10 for a typical daily move, capped at 20. Next it goes through signed_power with exponent 2 and pivot 10, so small rises give a very small short and sharp rises a large one: a 0.5x-typical rise gives 2.5, a typical rise gives 10, a 1.5x-typical rise gives 22.5. The sign is then flipped to short and the forecast is clipped to at most 0. The combined forecast is clipped to -20 overall. The position is held only for the bar after the qualifying close, unless the next bar qualifies again.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Confirm: The horizon is 1 bar (the next day). Pool all active bars across the 6 windows; each next-day return counts once, so none overlap. Before costs, the position-weighted mean next-day BTC return after active bars must be below the mean daily return over all bars of the same windows, with a t-statistic of 2 or more on at least 30 active bars. Supporting check: within the active bars, the strategy's next-day return grows with the size of the short (positive slope on |forecast|).
Reject: Before costs, the position-weighted mean next-day return after active bars is equal to or above the all-bar mean daily return (t-statistic of 0 or more). Equivalently, the short's pooled return relative to the all-bar baseline is zero or negative.
Inconclusive: Two cases neither confirm nor reject. The first is fewer than 30 active bars. The second is a shortfall below the all-bar mean that has the right sign but a t-statistic between 0 and 2.
Deviation: Four parts of the idea change in the config. - "Sharp" is not a threshold. Every up bar on below-average volume is traded, and sharpness only sets the size through signed_power. - "Unusually low volume" becomes "below the 20-day average". - "Followed by falling back" is tested only over the single next day, because the short exists only while the qualifying bar's condition holds. - The move is a one-day close-to-close change, not a multi-day rise.
