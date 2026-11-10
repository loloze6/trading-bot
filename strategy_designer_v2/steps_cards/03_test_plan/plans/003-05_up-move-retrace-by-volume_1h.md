---
idea: 003-05_up-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: Recompute at every 1h close. The move is the one-bar percent return, from PriceEvolutionComponent with period 1. Standardise it against the mean absolute value of the previous 60 values (min_periods 20). Clip it at 0, so only up bars count. Apply signed_power with exponent 2 and pivot 10, so small up bars are damped smoothly toward 0 and sharp ones are amplified. Volume sets the sign. If the bar's volume is below its 20-bar average (the volume_filter convention), the bar is "thin" and the forecast is minus this value: a short that grows with the size of the rise, betting on giveback. If volume is at or above its average, the bar is "heavy" and the forecast is plus this value: a long that grows with the size of the rise, betting on continuation. After a down or flat bar the forecast is 0. It is capped at ±20.
Config: 003-05_up-move-retrace-by-volume_1h_config.json
Confirm: Horizon 6 bars. Take every bar with a non-zero forecast and keep only events at least 6 bars apart, so no forward return is counted twice. Regress the forward 6-bar log return, minus the window's mean 6-bar return (the buy-and-hold drift), on two terms: the standardised move size, and the move size times a thin-volume dummy. The thin-volume interaction coefficient must be negative with t ≤ −2 on the pooled 6 windows, and negative in at least 4 of the 6 windows. That means thin up-moves give back more than heavy up-moves of the same size. Supporting check: the before-cost portfolio return in excess of position-weighted buy-and-hold is positive in at least 4 of 6 windows.
Reject: The pooled interaction coefficient is zero or positive (t > −1), meaning that, for the same move size, thin up-moves hold as well as heavy ones or better. The theory is also rejected if it is positive with t ≥ 2, meaning heavy moves revert more.
Inconclusive: The coefficient is negative with −2 < t ≤ −1. Or it is pooled-significant but negative in fewer than 4 of 6 windows.
Deviation: "Low or high volume" becomes a binary split of the move bar's volume at its 20-bar average, not a graded measure of how unusual it is. The "sharp move" is a single 1h bar, graded by size, with no size threshold. The config holds each position for only the one bar after the move, while the criterion reads a 6-bar forward return from the record. Down moves are not traded.
