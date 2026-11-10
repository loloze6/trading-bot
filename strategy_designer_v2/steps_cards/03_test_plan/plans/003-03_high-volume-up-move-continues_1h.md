---
idea: 003-03_high-volume-up-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: On each 1h bar, BTC/USDT is active only when two things hold at that bar's close. The bar closed up, so its 1-bar percent return is above 0. The bar's volume is at or above its own 20-bar average. On those bars the forecast is long and graded. It equals the bar's 1-bar percent return divided by the mean absolute 1-bar return of the 60 bars before it, times 10, capped at 20, and kept at 0 or above. A bar that rises by its usual absolute hourly move gives about +10 (100% long). A bar that rises twice as far or more gives up to +20. A tiny rise gives near 0. On every other bar the forecast is 0 (flat): a down bar, a flat bar, or a bar with volume below its 20-bar average. There is no short side.
Config: 003-03_high-volume-up-move-continues_1h_config.json
Confirm: Horizon is 1 bar. Take every bar with forecast > 0 and compute the next bar's close-to-close return minus that window's mean hourly return (the buy-and-hold drift). Pooled over the 6 windows, the mean of this excess return is > 0 with t-stat >= 2.0. The bars do not overlap, so each is counted once. Supporting check: regressing that excess next-bar return on the forecast size gives a positive slope, so larger high-volume up moves are followed by larger continuation.
Reject: The pooled mean excess next-bar return on active bars is <= 0. A t-stat <= -2.0 is a clearer rejection, because it means high-volume up moves revert, which the brief names explicitly as a refutation.
Inconclusive: The mean excess return is positive but its t-stat is below 2.0. Also inconclusive: the sign of the excess return splits 3–3 across the six windows, or the supporting slope has the opposite sign to the main mean.
Deviation: "Unusually high volume" becomes volume at or above its 20-bar mean, which is a looser bar than "unusual". "Sharp" is not a cut-off: any up bar on above-average volume is active, and sharpness only sets the position size. "Followed by price rising further" is measured only over the next 1h bar. The position exists only while the triggering bar's condition holds, so it is not held over a longer continuation.
