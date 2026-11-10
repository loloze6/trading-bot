---
idea: 003-06_down-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The forecast is non-zero only on a day that closes down, and the day's volume decides its sign. The drop is measured as the one-day percent change of the close (PriceEvolution, period 1). It is standardised against its own last 60 values (min 20), and then passed through signed_power (exponent 2, pivot 10), so small drops give small forecasts and sharp drops give larger ones. Two cases: - Thin drop: the day's volume is below its 20-day mean. The forecast is long and positive, a reversion bet, and grows with the square of the standardised drop. - Heavy drop: the day's volume is at or above its 20-day mean. The forecast is short and negative, a continuation bet, graded the same way. On up days and flat days the forecast is 0. Each position is held for the next day only, because the forecast is recomputed at the next close.
Config: 003-06_down-move-retrace-by-volume_1d_config.json
Confirm: The horizon is 1 bar (the next day), so returns do not overlap. On every active bar, take the position times the next-day return, minus the position times the coin's mean daily return over the same window, before costs. Pooled over the 6 windows, the mean of this excess return is above 0 with a t-statistic of at least 2, and it is positive in at least 4 of the 6 windows. Supporting check: the drop-size-weighted mean next-day return after thin drops is higher than after heavy drops.
Reject: The pooled mean excess return is 0 or below. This means that, for drops of the same size, heavy-volume drops are followed by returns as good as or better than thin-volume drops.
Inconclusive: The pooled mean excess return is positive but the t-statistic is below 2, or it is positive in fewer than 4 of the 6 windows.
Deviation: The config differs from the idea in four ways: - "Afterwards" becomes the next single day. - Low and high volume are a binary split at the 20-day mean volume, not graded by how unusual the volume is. - "Sharp" is a graded weight by drop size, not a threshold. - The idea compares how much of the drop is given back after thin and heavy drops. The config instead takes the next-day return as a long position after thin drops and a short position after heavy drops. A positive result therefore shows that the two groups differ in the predicted direction; it does not measure each group's share of the drop retraced.
