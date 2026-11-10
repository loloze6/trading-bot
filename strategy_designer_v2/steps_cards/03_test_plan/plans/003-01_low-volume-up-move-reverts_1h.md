---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: The forecast is active only on bars where the current 1h bar's volume is below its 20-bar mean, and it is 0 on all other bars. On an active bar, take the current bar's close-to-close return (PriceEvolution, period 1). Standardise it against its own last 60 values (min 20). Keep only the upward part (clip at 0), then apply signed_power with exponent 2 and pivot 10, so that sharp rises count much more than small ones. Finally negate it, giving a short position whose size grows with the square of the standardised rise. The forecast is 0 when the bar fell or was flat, and it is never positive.
Config: 003-01_low-volume-up-move-reverts_1h_config.json
Confirm: Horizon is 6 bars. Take each bar's excess return: BTC's close-to-close return over the next 6 bars minus that window's mean 6-bar return. Take the 10% of bars with the most negative forecast, counting each event once by skipping any bar within 6 bars of an earlier selected one. If their mean excess return is negative with t ≤ -2 pooled over all windows, and negative in at least 4 of 6 windows, the idea is confirmed. Supporting check: the strategy's pre-cost portfolio value ends above its start in at least 4 of 6 windows.
Reject: The idea is rejected if the mean 6-bar excess return after those largest short forecasts is zero or positive pooled (t > -1). It is also rejected if it is negative in 2 or fewer of the 6 windows.
Inconclusive: A pooled t between -2 and -1, or a negative pooled mean that holds in only 3 of 6 windows. Also inconclusive: fewer than 30 non-overlapping events in total.
Deviation: "Unusually low volume" becomes a binary condition: the bar's volume is below its 20-bar mean. "Sharp upward move" becomes the single current bar's rise, made graded by squaring its standardised size. "Followed by" is held only while the bar's volume stays below its mean, so the position usually lasts one bar. The 6-bar reversion is judged from the recorded forecast and the following prices, not from the position itself. The brief's contrast with high-volume moves is not tested here.
